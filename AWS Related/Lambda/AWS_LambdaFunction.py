import boto3
import json

ec2 = boto3.client('ec2', region_name='us-east-1')

INSTANCE_ID = 'i-0f4[corrupted]fab'

def get_instance_state(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['State']['Name']

def start_instance_if_stopped(instance_id):
    instance_state = get_instance_state(instance_id)
    print(f"Current State: {instance_state}")
    if instance_state == 'stopped':
        ec2.start_instances(InstanceIds=[instance_id])
        print('Starting the instance')
        return {
            'status': 200,
            'body': 'Unity Builder Started'
        }
    else:
        print(f'Instance is still in phase: {instance_state}')
        return {
            'status': 200,
            'body': f'Instance is still in phase: {instance_state}'
        }

def lambda_handler(event, context):
    http_method = "GET"
    if "context" in event:
        http_method = event["context"]["http-method"]
        
    if http_method == "GET":
        #queryParams = event.get("params", {}).get("querystring", {})
        if 1 == 1 or "build" in queryParams and queryParams["build"]:
            print('GET request with build parameter')
            return start_instance_if_stopped(INSTANCE_ID)
        else:
            print('Invalid GET method')
            return {
                'status': 400,
                'body': 'Invalid GET method'
            }
    elif http_method == "POST":
        body = event.get("body-json", {})
        plasticComment = body.get("PLASTIC_LABEL_NAME", "")
        if "BUILD" in plasticComment:
            print('POST request with valid PLASTIC_LABEL_NAME')
            return start_instance_if_stopped(INSTANCE_ID)
        else:
            print('Invalid event or commit message does not contain "BUILD"')
            return {
                'status': 400,
                'body': 'Invalid event or commit message does not contain "BUILD"'
            }
    else:
        print('Invalid HTTP method')
        return {
            'status': 400,
            'body': 'Invalid HTTP method'
        }
