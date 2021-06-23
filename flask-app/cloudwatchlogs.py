import boto3
import botocore
from datetime import datetime


class Cloudwatchlogs:

    # Create a list of of the folders of last 5 CloudWatch log streams
    def create_folder_list():
        # Instantiate log client
        client = boto3.client('logs')

          # Get the last 5 log streams for CloudWatch
        try:
            resp = client.describe_log_streams(
                logGroupName='/aws/connect/joshweepie',  orderBy='LastEventTime', descending=True, limit=5)
        except client.exceptions.ResourceNotFoundException as error:
            print(error.response['Error'])

        try:
            # Create a list of the last 5 CloudWatch log stream names
            log_folders = []
            for log_stream in resp["logStreams"]:
                latestlogStreamName = log_stream["logStreamName"]
                log_folders.append(latestlogStreamName)
        except:
            e = "Couldn't create the folder list because of Boto error"
            return e
        return log_folders

    # Query the logs of an indivdual folder and save a dictionary with the callers phone number, timestamp, and generated name
    def query_logs(folder):
        # Instantiate log client
        client = boto3.client('logs')

        # Find the log stream
        try:
            response = client.filter_log_events(
                logGroupName='/aws/connect/joshweepie',
                logStreamNames=[folder],
                filterPattern="calling_phone_number"
            )
        except client.exceptions.ResourceNotFoundException as error:
            print(error.response['Error'])

        try:
            # Convert the 'message' in the response because it's returned as a string and not a dictionary
            response_dict = eval(response["events"][0]["message"])

            # Find the log event in the Cloudwatch log stream that contains the callers phone number and generated name
            phone = response_dict['ExternalResults']['calling_phone_number']
            time = response_dict['Timestamp']
            timestamp = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fz')
            date = timestamp.strftime("%m-%d-%Y %H:%M:%S UTC")
            first_name = response_dict['ExternalResults']['first_name']
            last_name = response_dict['ExternalResults']['last_name']
            full_dict = {'phone': phone, 'time': date, 'first_name': first_name,
                        'last_name': last_name}

        except Exception as error:
            response = client.filter_log_events(
                logGroupName='/aws/connect/joshweepie',
                logStreamNames=[folder])
            # Convert the 'message' in the response because it's returned as a string and not a dictionary
            response_dict = eval(response["events"][0]["message"])
            # Fetch and return formatted time along with a message that there is a data format issue in the logs to evaluate
            time = response_dict['Timestamp']
            timestamp = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fz')
            date = timestamp.strftime("%m-%d-%Y %H:%M:%S UTC")
            error_dict = {'phone': 'Not Available', 'time': date, 'first_name': 'Not Available',
                          'last_name': 'Not Available'}
            return error_dict

        return full_dict

    # Get the data we need from each individual log stream folder using the query_logs function
    def get_all_data():
        x = (Cloudwatchlogs.create_folder_list())
        result1 = Cloudwatchlogs.query_logs(x[0])
        result2 = Cloudwatchlogs.query_logs(x[1])
        result3 = Cloudwatchlogs.query_logs(x[2])
        result4 = Cloudwatchlogs.query_logs(x[3])
        result5 = Cloudwatchlogs.query_logs(x[4])
        return result1, result2, result3, result4, result5
