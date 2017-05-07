from __future__ import print_function

import boto3
import os
from decimal import Decimal
import json
import urllib

print('Loading function')

REKOGNITION = boto3.client('rekognition')
QUEUE_URL = os.getenv("QUEUE_URL")
SQS = boto3.client("sqs")


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_labels(bucket, key):
    response = REKOGNITION.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key)

        # Print response to console.
        print(response)
        
        labels = response
        SQS.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps({'PK': key, 'Labels': labels}))

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
