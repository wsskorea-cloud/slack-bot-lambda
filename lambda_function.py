import json
import os
import requests


def lambda_handler(event, context):
    sqs_message = event.get('Records')[0]
    sqs_message = sqs_message.get('body')
    sqs_message = json.loads(sqs_message)

    SLACK_URL = os.getenv('SLACK_URL')

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "{}".format(sqs_message.get('title'))
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Type:*\n{}".format(sqs_message.get('type'))
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*When:*\n{}".format(sqs_message.get('when'))
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Where:*\n{}".format(sqs_message.get('where'))
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Log*:\n```{}```".format(sqs_message.get('log'))
                    }
                ]
            }
        ]
    }

    r = requests.post(
        SLACK_URL,
        json.dumps(payload)
    )

    print(payload)

    return {
        'statusCode': r.status_code,
        'body': r.content.decode('UTF-8')
    }


# Development Environment Only
if __name__ == '__main__':
    event = {
        "Records": [
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": "{\"title\": \"Slack Bot Test\",\"type\": \"Information\",\"when\": "
                        "\"2022-06-20T09:00:00+09:00\",\"where\": \"Postfix\",\"log\": \"TRACE\\nBACK\"}",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001"
                },
                "messageAttributes": {},
                "md5OfBody": "{}",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1"
            }
        ]
    }

    print(lambda_handler(event, None))
