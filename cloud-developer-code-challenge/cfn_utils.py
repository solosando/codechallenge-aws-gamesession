import os
import json
import boto3
import logging
import ast
import sys
from typing import Dict, List

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_new_s3_bucket(bucket_name: str, s3=boto3.client("s3")):
    """
    Function to create a new S3 bucket.

    :param bucket_name: The name of the bucket to be created
    """

    try:
        # Creating the bucket
        s3.create_bucket(Bucket=bucket_name)

        print(f"Bucket {bucket_name} created.")

    except Exception as e:
        print(f"Error while creating the bucket: {e}")


def upload_file_to_s3(file_name, bucket_name, object_name=None, s3=boto3.client("s3")):
    """
    Function to upload a file to an existing S3 bucket.

    :param file_name: The relative path of the file to be uploaded
    :param bucket_name: The name of the bucket where the file should be uploaded
    :param object_name: The name of the object in the bucket, if different from the file name
    """

    if object_name is None:
        object_name = file_name

    try:
        # Uploading the file
        s3.upload_file(file_name, bucket_name, object_name)

        print(
            f"File {file_name} was uploaded to bucket {bucket_name} with name {object_name}"
        )

    except Exception as e:
        print(f"Error while uploading the file: {e}")


def create_stack(
    stack_name: str,
    template_body: str,
    required_capabilities: list,
    event_bus_name: str,
    table_name: str,
    bucket_name: str,
    file_name: str,
) -> bool:
    """
    Create a CloudFormation stack with the specified parameters.

    :param stack_name: The name of the stack to create.
    :param template_body: The body of the CloudFormation template.
    :param required_capabilities: The capabilities required for stack creation.
    :param event_bus_name: The name of the event bus to be created in the CloudFormation stack.
    :param table_name: The name of the DynamoDB table to be created in the CloudFormation stack.
    :param bucket_name: The name of the S3 bucket to be created in the CloudFormation stack.
    :param file_name: The name of the file to be uploaded to the S3 bucket.
    :return: True if the stack creation is successful, False otherwise.
    """
    cloudformation_client = boto3.client("cloudformation")
    try:
        # Create the stack
        create_stack_response = cloudformation_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=required_capabilities,
            Parameters=[
                {
                    "ParameterKey": "EventBusName",
                    "ParameterValue": event_bus_name,
                },
                {
                    "ParameterKey": "TableName",
                    "ParameterValue": table_name,
                },
                {
                    "ParameterKey": "MyBucket",
                    "ParameterValue": bucket_name,
                },
                {
                    "ParameterKey": "S3Key",
                    "ParameterValue": file_name,
                },
            ],
        )
        stack_id = create_stack_response["StackId"]
        logging.info(f"Stack {stack_name} creation request ID: {stack_id}")

        # Wait for the stack to be created
        cloudformation_client.get_waiter("stack_create_complete").wait(
            StackName=stack_name
        )

        # Check if the stack creation was successful
        stack_description = cloudformation_client.describe_stacks(StackName=stack_name)
        if stack_description["Stacks"][0]["StackStatus"] == "CREATE_COMPLETE":
            return True
        else:
            logging.error(
                f"Stack {stack_name} creation failed with status: {stack_description['Stacks'][0]['StackStatus']}"
            )
            return False

    except Exception as e:
        logging.error(f"Error creating stack {stack_name}: {e}")
        return False


def put_events(folder_path: str, eventbridge_client=boto3.client("events")) -> bool:
    """
    Send a batch of events to EventBridge from the given folder path.

    Parameters:
    folder_path (str): The path to the folder containing event files.
    eventbridge_client (boto3.client): A preconfigured EventBridge client.

    Returns:
    bool: True if all events were sent successfully; False otherwise.
    """
    batch_size = 10
    total_files = count_files(folder_path)

    try:
        for i in range(0, total_files, batch_size):
            batch = load_batch_events(folder_path, i, batch_size)
            send_events(batch, eventbridge_client)
    except Exception as e:
        logging.error(f"An error occurred while sending events: {str(e)}")
        return False

    return True


def count_files(folder_path: str) -> int:
    """
    Count the number of files in the given folder path.

    Parameters:
    folder_path (str): The path to the folder containing event files.

    Returns:
    int: The number of files in the folder.
    """
    return sum(
        len(files) for root, dirs, files in os.walk(folder_path) if root == folder_path
    )


def load_batch_events(folder_path: str, start_index: int, batch_size: int) -> list:
    """
    Load a batch of event files from the given folder path.

    Parameters:
    folder_path (str): The path to the folder containing event files.
    start_index (int): The index of the first file to load.
    batch_size (int): The number of files to load.

    Returns:
    list: A list of event dictionaries.
    """
    events = []
    for i, file in enumerate(os.listdir(folder_path)):
        if i >= start_index and i < start_index + batch_size:
            with open(os.path.join(folder_path, file), "r") as f:
                event = json.load(f)
                # Create a new event dictionary with only the valid keys and values
                new_event = {}
                for key in ["Source", "Resources", "DetailType", "Detail"]:
                    value = event.get(key)
                    if value is not None:
                        new_event[key] = value
                events.append(new_event)
    return events


def send_events(events: list, eventbridge_client=boto3.client("events")) -> None:
    """
    Send a batch of events to EventBridge.

    Parameters:
    events (list): A list of event dictionaries.
    eventbridge_client (boto3.client): A preconfigured EventBridge client.

    Returns:
    None
    """
    entries = [event for event in events]
    response = eventbridge_client.put_events(Entries=entries)

    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
        raise Exception("An error occurred while sending events to EventBridge.")


def main(
    bucket_name,
    file_name,
    template_body,
    stack_name,
    required_capabilities,
    event_bus_name,
    table_name,
    events_dir,
):
    """
    Main function to verify the CloudFormation stack and put events on EventBridge.

    Parameters:
    stack_name (str): The name of the CloudFormation stack to be deployed.
    events_dir (str): The path to the directory containing the JSON files with event details.
    Returns:
    None
    """

    # Create S3 bucket
    create_new_s3_bucket(bucket_name)

    # Upload lambda code to bucket
    upload_file_to_s3(file_name, bucket_name)

    # Create stack using AWS CloudFormation
    create_stack(
        stack_name,
        template_body,
        required_capabilities,
        event_bus_name,
        table_name,
        bucket_name,
        file_name,
    )

    # Put events on EventBridge
    put_events(events_dir)
    batch_size = count_files(events_dir)
    events = load_batch_events(events_dir, start_index=0, batch_size=batch_size)
    send_events(events)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bucket-name",
        required=True,
        help="The name of the s3 bucket to be created",
    )
    parser.add_argument(
        "--file-name",
        required=True,
        help="The path to the directory containing the .zip file with lambda code",
    )
    parser.add_argument(
        "--stack-name",
        required=True,
        help="The name of the cloudformation stack to be created",
    )
    parser.add_argument(
        "--template-body",
        required=True,
        help="The yaml file with the stack resources to be crated",
    )
    parser.add_argument(
        "--capabilities",
        required=True,
        help="The capabilities for the cloudformation stack",
    )
    parser.add_argument(
        "--event-bus-name",
        required=True,
        help="Name of the event bus name  where the events will be sent",
    )
    parser.add_argument(
        "--table-name",
        required=True,
        help="Name of the dynamodb table where the events will be stored",
    )
    parser.add_argument(
        "--events-dir",
        required=True,
        help="The path to the directory containing the JSON files with event detailsk",
    )

    args = parser.parse_args()
    main(
        args.bucket_name,
        args.file_name,
        args.stack_name,
        args.template_body,
        args.required_capabilities,
        args.event_bus_name,
        args.table_name,
        args.events_dir,
    )
    sys.exit(0)
