import pika
import sys
import webbrowser
import csv
import time
import logging

# Specify the log file path
LOG_FILE = "Cell-Data.log"

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),  # Log to a file
        logging.StreamHandler()  # Show message stream on the console
    ]
)

# Declare program constants
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
CELL_DATA_FILE_NAME = "Cell_Data.csv"
SHOW_OFFER = True  # Control whether to show the RabbitMQ Admin webpage offer

def admin():
    """Offer to open the RabbitMQ Admin website"""
    global SHOW_OFFER
    if SHOW_OFFER:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(channel, queue_name, timestamp, cell_density, o2_levels, co2_levels):
    """Send a message to the specified queue.
    Display a message regarding what queue was accessed and the data being sent.
    
    Parameters (all fed in from the main() function):
        channel
        queue_name
        timestamp
        cell_density
        o2_levels
        co2_levels
    """
    message = f"{timestamp},{cell_density},{o2_levels},{co2_levels}"
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    logging.info(f"Sent: Timestamp={timestamp}, Cell Density={cell_density}, O2 Levels={o2_levels}, CO2 Levels={co2_levels}")

def main():
    """
    Delete existing queues.
    Declare new queues.
    Read from csv file.
    Send messages to queue based on the data columns in the csv.
    This process runs and finishes.
    """

    try:
        # Create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        # Use the connection to create a communication channel
        ch = conn.channel()
        # Delete the queues if they exist
        for queue_name in ["cell-density", "o2-levels", "co2-levels"]:
            ch.queue_delete(queue=queue_name)
        # Use the channel to declare durable queues
        for queue_name in ["cell-density", "o2-levels", "co2-levels"]:
            ch.queue_declare(queue=queue_name, durable=True)

        # Initialize variables for alerts
        o2_alert_count = 0
        cell_density_alert_triggered = False
        last_timestamp = None

        # Open and read the CSV file
        with open(CELL_DATA_FILE_NAME, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row if it exists

            for row in reader:
                timestamp, cell_density, o2_levels, co2_levels = map(float, row[0:4]) if row[0:4] else (None, None, None, None)

                # Check if the timestamp has changed
                if timestamp != last_timestamp:
                    send_message(ch, "Cell_Data", timestamp, cell_density, o2_levels, co2_levels)
                    last_timestamp = timestamp

                # Alerts
                if o2_levels < 38:
                    logging.info("Alert: O2 levels are less than 38 ppm. Check O2 system.")
                    o2_alert_count = 0
                if o2_levels > 41:
                    logging.info("Alert: O2 levels are greater than 41 ppm. Check O2 system.")
                    o2_alert_count = 0

                if cell_density is 2.0:
                    logging.info("Alert: Cell Density is = 2.0. Remove from Incubator Cells are ready to be used.")
                    cell_density_alert_triggered = True
                if co2_levels > 17:
                    logging.info("Alert: CO2 levels are > 17 ppm . CO2 levels rising to dangerous levels.")

                # Check for Cell Density drop alert
                if cell_density_alert_triggered and cell_density < 1.7:
                    logging.info("Alert: Cell Density dropped below 1.7 after reaching 2.0. Discard cells.")
                    cell_density_alert_triggered = False

                # Sleep for 1 second before processing the next row
                time.sleep(1)

    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Program execution was canceled by the user.")
    finally:
        # Close the connection to the server
        conn.close()

# Standard Python idiom to indicate the main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # Open the RabbitMQ Admin site
    admin()

    # Call the custom function to read and send data from the CSV
    main()
