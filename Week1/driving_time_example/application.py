import datetime
from flask import Flask
from flask import render_template, render_template_string, redirect
import simplejson
import urllib.request
import boto3
import time

from user_definition import *

application = Flask(__name__)

def read_s3_obj(bucket_name, output_file):
    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name, output_file)
        body = obj.get()['Body'].read().decode('utf-8')
        return body
    except:
        return ""



@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    #body = read_s3_obj(bucket_name, output_file)

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, output_file)
    body = obj.get()['Body'].read().decode('utf-8')

    return render_template('index.html', s3=s3, obj=obj, output=body)


@application.route('/calculate', methods=['GET', 'POST'])
def calculate():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?key={0}&origins={1}&destinations={2}&mode=driving&departure_time=now&language=en-EN&sensor=false".format(str(apikey), str(orig_coord), str(dest_coord))
    # example result json : https://maps.googleapis.com/maps/api/distancematrix/json?key=AIzaSyCSX1AjP3IMYq9CsrjiAh5RqlFyBd5uJW8&origins=37.7909,-122.3925&destinations=37.7765,-122.4506&mode=driving&departure_time=now&language=en-EN&sensor=false
    result = simplejson.load(urllib.request.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
    leave = "Don't leave yet"
    if(int(driving_time.split("mins")[0].strip()) < 20):
        leave = "Leave"
    prev_reading = read_s3_obj(bucket_name, output_file)
    print(prev_reading)

    body = "{}\t{}\t{}\t{}\t{}\t\n{}".format(leave,
                                             datetime.datetime.now(),
                                             result['origin_addresses'][0],
                                             result['origin_addresses'][0],
                                             driving_time,
                                             prev_reading)


    s3 = boto3.resource("s3").Object(bucket_name,output_file).put(Body=body)

    time.sleep(5) # Added this for working on EB - Needs a delay to  update the access after putting an obj

    return redirect("/index")

if __name__ == '__main__':
    application.jinja_env.auto_reload = True
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.debug = True
    application.run()
