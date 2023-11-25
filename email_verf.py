import boto3


def send_email(recipient, code):
    # client for sns
    sns = boto3.client('sns', region_name='us-east-1')
    sender_email_address = "none"
    recipient_email_address = recipient
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:548277993345:email_verification',
        Message=f"{sender_email_address} {recipient_email_address} {code}"
    )

    # Print out the response
    print(response)
