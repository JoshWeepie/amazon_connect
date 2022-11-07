Introduction
------------

Amazon Connect phone number: 1-845-318-2265

Web app to display last 5 callers and randomly generated name: https://connect.joshweepie.com/

EC2 Diagram
-------------
![EC2 Diagram](https://github.com/JoshWeepie/amazon_connect/blob/main/architecture.PNG)

ECS Digram
-------------
![ECS Diagram](https://github.com/JoshWeepie/amazon_connect/blob/main/alb_ecs.PNG)

Lambda function
-------------
[Lambda function](https://github.com/JoshWeepie/amazon_connect/blob/main/lambda/lambda.py)

In the lambda function, I fetch the calling phone number from the Amazon Connect [JSON](https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html#function-contact-flow) request and
generate a first name and last name with the [names](https://pypi.org/project/names/) package. Next, the function retrieves the DynamoDB [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html) service resource 
and sets the DynamoDB table for the project, and lastly inserts the calling phone number, date, first name, and last name that was generated for the caller into DynamoDB.

Contact Flow
-------------
![Contact Flow](https://github.com/JoshWeepie/amazon_connect/blob/main/contact_flow.PNG)

The contact flow first enables logging, then invokes the Lambda function to randomly generate a name. The name is then stored in DynamoDB along with the caller's phone number,
and then can be retrieved and repeated back to the caller if they follow the prompt.

Web App and CloudWatch log parsing
-------------
The web app is a simple Flask web app uploaded to an Ubuntu EC2 instance with Nginx as the web server. I assigned an Elastic IP and used my domain in Route 53 to create the DNS A record. 

I made a simple library [cloudwatchlogs.py](https://github.com/JoshWeepie/amazon_connect/blob/main/flask-app/cloudwatchlogs.py) file that queries logs in the CloudWatch AWS Connect log group log streams using the Boto3 [CloudWatchLogs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#cloudwatchlogs)
client. The library filters based on the filter pattern "calling_phone_number", and returns the results in a dictionary that is fetched with the 
"home" function in application.py, and then is parsed by Jinja in the home.html file.
