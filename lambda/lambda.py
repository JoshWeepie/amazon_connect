import boto3
import os
from package import names
from datetime import datetime

def lambda_handler(event, context):

    # Fetch the calling phone number from the Amazon Connect JSON reqeuest
    digits = event['Details']['ContactData']['CustomerEndpoint']['Address']

    # Get the DB name from environment variable
    db_name = os.environ.get('db_name')

    # Get the DynamoDB service resource
    dynamodb = boto3.resource('dynamodb')

    # Set the table name 
    table = dynamodb.Table(db_name)

    # Check if the phone number already exists in the table
    response = table.get_item(Key={'Calling Number': digits})
    item = response.get('Item')
    if item:
        # If the phone number already exists, use the first name and last name from the existing entry
        first_name = item['First Name']
        last_name = item['Last Name']
        
         # Save the date
        now = datetime.now()
        date = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Insert the phone number and first and last names into the DB
        table.put_item(Item={'Calling Number': digits,
                             'First Name': first_name,
                             "Last Name": last_name,
                             "Date": date})

    else:
        # If the phone number does not exist, generate a random name for example data
        first_name = names.get_first_name()
        last_name = names.get_last_name()

        # Save the date
        now = datetime.now()
        date = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Insert the phone number and first and last names into the DB
        table.put_item(Item={'Calling Number': digits,
                             'First Name': first_name,
                             "Last Name": last_name,
                             "Date": date})

    # The Amazon Connect consumer will only accept a flat response of key-value pairs, not nested JSON
    return {
        'calling_phone_number': digits,
        'first_name': first_name,
        'last_name': last_name,
    }
