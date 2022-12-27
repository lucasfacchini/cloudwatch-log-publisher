import base64
import gzip
import json
import os
from io import BytesIO

from slack_sdk import WebClient

SLACK_BOT_TOKEN=os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL=os.getenv('SLACK_CHANNEL')


def receive_log(event, *_):
    encoded_data = str(event['awslogs']['data'])
    json_logs = gzip.GzipFile(fileobj=BytesIO(base64.b64decode(encoded_data, validate=True))).read()
    log_data = json.loads(json_logs)

    client = WebClient(token=SLACK_BOT_TOKEN)

    for log_event in log_data['logEvents']:
        client.chat_postMessage(channel=SLACK_CHANNEL,
                                text=f"*{log_event['message'].strip()}* | {log_data['logGroup']}")
