import boto3
import json

class Job:
    def __init__(self, data):
        self.data = data

    def dispatch(self, queue_url):
        sqs = boto3.client('sqs')
        message_body = json.dumps({'job': self.__class__.__name__, 'data': self.data})
        sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
        raise NotImplementedError("Subclasses must implement this method")
