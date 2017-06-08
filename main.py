from __future__ import print_function
import boto3
import json
from urllib2 import Request, urlopen, URLError, HTTPError
import logging
from botocore.exceptions import ClientError
import os
from base64 import b64decode
import chef

# CHEF_URL, SLACK_HOOK,user and region should be set to some value
# in get_pem we encrypt chef key.
# Function requires IAM role with ec2 tag read permission and Chef user with org
# admin permissions
# Tested against Chef 12

CHEF_URL=''
HOOK
user = ''
instancename = ''
region = ''

# KMS
def get_pem():
    try:
        with open('encrypted_pem.txt', 'r') as encrypted_pem:
            pem_file = encrypted_pem.read()

        kms = boto3.client('kms', region_name=region)
        return kms.decrypt(CiphertextBlob=b64decode(pem_file))['Plaintext']
    except (IOError, ClientError, KeyError) as err:
        LOGGER.error(err)
        return False

# Find instance tag key 'Name' and return value form aws instance-id
def get_instance_tag(instancename):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(instancename)
    tags = ec2instance.tags

    for i in tags:
        if i['Key'] == 'Name':
            name = i['Value']
    return name

# Chef
def lambda_handler(event, context):
    instanceState = event["detail"]["state"]
    instanceId = event["detail"]["instance-id"]
    get_pem()
    get_instance_tag(instanceId)
    with chef.ChefAPI(CHEF_URL, get_pem(), user):
        node = chef.Node(get_instance_tag(instanceId))
        node.delete()
# SLACK
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    slack_message = {
      'channel': "devops",
      'userame': 'awsbot',
      'mrkdwn': 'true',
      'text': "Instance *%s*\nEntered *%s* state\n Removed from Chef" % (get_instance_tag(instanceId), instanceState)
    }
    hook = SLACK_HOOK
    req = Request(hook, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

    return 'Hello from Lambda'
