import boto3
from cloudwatchlogs import Cloudwatchlogs
from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def home():
    phones = Cloudwatchlogs.get_all_data()
    return render_template("home.html", phones=phones)


if __name__ == "__main__":
    application.run()
