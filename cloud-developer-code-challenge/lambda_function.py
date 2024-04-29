import json
import boto3

# Initialize the EventBridge client
eventbridge = boto3.client("events")

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-game-session-table")


def get_requested_event(events):
    """Get the requested event from the list of events."""
    return next(
        (e for e in events if e["detail-type"] == "game-session-request.requested"),
        None,
    )


def save_game_session(event):
    """Save the game session details to the DynamoDB table."""
    request_event = get_requested_event(event["detail"]["gameSessionRequestEvents"])

    if not request_event:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing game session request or started event"),
        }

    # Extract the relevant information from the requested event
    game_session_details = request_event["detail"]["gameDetails"]
    table.put_item(Item=game_session_details)

    # Check if the information is already recorded in the table
    response = table.get_item(Key={"hostname": game_session_details["hostname"]})

    return response


def handle_game_session_request(event):
    """Handle the game session request and send the finished event to the event bus."""
    response = save_game_session(event)

    if response.get("Item"):
        # Send the finished event to the event bus
        eventbridge.put_events(
            Entries=[
                {
                    "Source": "my-event-bus",
                    "DetailType": "game-session-request.finished",
                    "Detail": json.dumps(event),
                }
            ]
        )
    else:
        # Send the failed event to the event bus
        eventbridge.put_events(
            Entries=[
                {
                    "Source": "my-event-bus",
                    "DetailType": "game-session-request.failed",
                    "Detail": json.dumps(event),
                }
            ]
        )


def lambda_handler(event, context):
    """Handle the game session request in the Lambda function."""
    return handle_game_session_request(event)
