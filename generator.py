# Import required libraries for the project
import os
import boto3
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

# We used Load environment variables from .env file
load_dotenv()

# To Get the Kinesis stream name and AWS region from environment variables
STREAM_NAME = os.environ["STREAM_NAME"]
AWS_REGION = os.environ["AWS_REGION_GENERATOR"]

# We use to Initialize the Kinesis client using boto3
try:
    kinesis = boto3.client('kinesis', region_name=AWS_REGION)
    print(f"Successfully connected to Kinesis in region {AWS_REGION}.\n")
except Exception as e:
    print("Failed to connect to Kinesis:", str(e))
    exit(1)

# We using this Function to generate fake sensor data
def generate_data():
    data = {
        "sensor_id": random.randint(1, 4),
        "temperature": random.uniform(20.0, 30.0),
        "humidity": random.uniform(30.0, 50.0),
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

    print("\n🔧 Generated Sensor Data:")
    print("Sensor ID:", data["sensor_id"])
    print("Temperature:", round(data["temperature"], 2))
    print("Humidity:", round(data["humidity"], 2))
    print("Timestamp:", data["timestamp"])

    return data

# We are using Infinite loop to send data every 5 seconds
while True:
    data = generate_data()
    print(f"Sending data to Kinesis stream: {STREAM_NAME}")

    try:
        response = kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(data),
            PartitionKey=str(data["sensor_id"])
        )
        print("Data sent successfully | Record ID:", response['SequenceNumber'])

    except (BotoCoreError, ClientError) as e:
        print("Error sending data to Kinesis:", str(e))

    time.sleep(5)
