# Cell Data Monitoring and Alerting System
Author: Mike Abbinante
Date: 05Oct23

# Overview
The Cell Data Monitoring and Alerting System is a Python-based project designed for monitoring and managing cell culture data in a laboratory environment. This system reads cell culture data from a CSV file, sends it to RabbitMQ queues for further processing, logs events, and triggers alerts based on specific conditions. It's a valuable tool for researchers and lab technicians working with cell cultures to maintain optimal conditions and ensure the safety of experiments.

# Features
- Reads cell culture data from a CSV file, including timestamp, cell density, oxygen (O2) levels, and carbon dioxide (CO2) levels.
- Sends cell culture data to RabbitMQ queues, categorizing the data into "cell-density," "o2-levels," and "co2-levels" queues.
- Logs cell culture events, including messages sent to queues, alerts, and other relevant information, into a log file ("Cell-Data.log").
- Monitors cell culture parameters and triggers alerts for specific conditions.
- Option to open the RabbitMQ Admin webpage for queue monitoring.
# Prerequisites
Before setting up and running the project, ensure you have the following prerequisites:

-Python 3.x installed.
- RabbitMQ server installed and running.
- Access to a CSV file with cell culture data in the following format:
csv

# Project Tasks
The project will perform the following tasks:

- Establish a connection to the RabbitMQ server.
- Delete any existing queues with specific names ("cell-density," "o2-levels," "co2-levels").
- Declare durable queues for each type of cell culture data.
- Read data from the CSV file, send it to the appropriate RabbitMQ queue, and log events.
- Check for cell culture alerts (e.g., low O2 levels, high CO2 levels, cell density) and log them accordingly.
- Output detailed logs, including messages sent to queues, temperature alerts, and other events, into a log file ("Cell-Data.log").
