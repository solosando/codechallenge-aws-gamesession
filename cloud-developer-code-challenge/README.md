# cloud-developer-code-challenge
Minecloudcraft - Cloud Developer - Code Challenges Placeholder

## Code Challenge (A)

### Objective
Your task is to demonstrate your skills in using Infrastructure as Code (IaC) to automate cloud resources provisioning. You will create a project on GitHub that provisions an AWS Step Function (Express) in AWS, integrating with other AWS services to simulate a game session workflow.

### Requirements

1. Infrastructure as Code: Utilize an IaC tool of your choice (e.g., AWS CloudFormation, Terraform) to provision the required AWS resources. Your code should be well-organized, commented, and follow best practices.
2. AWS Step Function (Express): Create an AWS Step Function (Express) that orchestrates the following workflow, which should be triggered by the reception of a **game-session-request.requested** event on the custom event bus `my-event-bus`:
    - Event Publishing:
At the start of the workflow, publish an event `game-session-request.started` to a custom event bus named `my-event-bus`.
    - DynamoDB Interaction: Insert an object into a DynamoDB table named my-dynamo-db-table. The object should describe a game session, including fields like hostname, players, map, and mode.
    - Error Handling: In case of any errors during the workflow, publish a game-session-request.failed event to my-event-bus.
    - Success Completion: Upon successful completion of the workflow, publish a game-session-request.finished event to my-event-bus.
3. Event Examples:

    - **game-session-request.requested**

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-request.requested",
  "detail": {
    "sessionId": "<unique_session_id>",
    "gameDetails": {
      "hostname": "<hostname>",
      "players": <number_of_players>,
      "map": "<game_map>",
      "mode": "<game_mode>"
    }
  }
}
```
- **game-session-request.started**
```json
{
  "source": "code-challenge",
  "detail-type": "game-session-request.started",
  "detail": {
    "sessionId": "<unique_session_id>"
  }
}
```
- **game-session-request.failed**
```json
{
  "source": "code-challenge",
  "detail-type": "game-session-request.failed",
  "detail": {
    "sessionId": "<unique_session_id>",
    "error": "<error_message>"
  }
}
```
- **game-session-request.finished**
```json
{
  "source": "code-challenge",
  "event": "game-session-request.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "gameDetails": {
      "hostname": "<hostname>",
      "players": <number_of_players>,
      "map": "<game_map>",
      "mode": "<game_mode>"
    }
  }
}
```

### Submission Guidelines

- Fork this GitHub repository
- Ensure your project is well-documented, explaining how to deploy and test your infrastructure.
- Once completed, submit a pull request to the main repository with your changes.
- Include a `NOTES.md` in your project detailing your approach, any assumptions made, and instructions on how to execute your IaC scripts.

### Evaluation Criteria

- Code Quality: Clarity, maintainability, and adherence to IaC best practices.
- Functionality: The AWS resources are provisioned as per the requirements, and the Step Function workflow executes correctly upon receiving the game-session-request.requested event.
- Documentation: Clear instructions and explanations in your project's NOTES.md.

## Code Challenge (B) - Notification Service Integration

### Objective
Demonstrate your ability to integrate AWS services by creating a workflow that notifies players when a game session is created. This challenge involves working with AWS Step Functions, Amazon SNS, and AWS Lambda.

### Requirements

1. Infrastructure as Code: Use your preferred IaC tool to provision AWS resources. Structure your code clearly and follow best practices.
2. AWS Step Function: Set up an AWS Step Function triggered by the `event game-session-creation.finished` to custom event bus named `my-event-bus`. The workflow should:
    - Invoke an AWS Lambda function that publishes a message to an Amazon SNS topic named `some-sns-topic`. The message should inform players about the game session creation.
3. Error Handling: Implement error handling to publish a `notify-player-workflow.failed` event to `my-event-bus` in case of any failures.
4. Success Completion: On successful notification, publish a `notify-player-workflow.finished` event to my-event-bus.

### Example of events

Event Examples:

- **game-session-creation.finished**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-creation.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "gameDetails": {
      "hostname": "<hostname>",
      "players": <number_of_players>,
      "map": "<game_map>",
      "mode": "<game_mode>"
    }
  }
}
```

- **notify-player-workflow.started**:

```json
{
  "source": "code-challenge",
  "detail-type": "notify-player-workflow.started",
  "detail": {
    "sessionId": "<unique_session_id>"
  }
}
```

- **notify-player-workflow.failed**:

```json
{
  "source": "code-challenge",
  "detail-type": "notify-player-workflow.failed",
  "detail": {
    "sessionId": "<unique_session_id>",
    "error": "<error_message>"
  }
}
```

- **notify-player-workflow.finished**:

```json
{
  "source": "code-challenge",
  "detail-type": "notify-player-workflow.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "message": "Game session notification sent successfully."
  }
}
```

### Submission Guidelines
Follow the same guidelines as provided in the Code Challenge (A), focusing on the integration of Amazon SNS for player notifications.

## Code Challenge (C) - Payment Gateway Integration

### Objective
Showcase your skills in integrating external APIs with AWS by creating a workflow that charges for a game session once it's finished. This challenge will involve AWS Step Functions, AWS Lambda, and external API interaction.

### Requirements

1. Infrastructure as Code: Use IaC tools to provision the necessary AWS resources. Ensure your code is organized and adheres to industry standards.
AWS Step Function: Create a Step Function that is initiated by the `game-session.finished` event on custom event bus named `my-event-bus`. The workflow should:
    - Call an external payment gateway API (https://payment-gateway.example/charge) to charge for the game session. You can simulate this by integrating with an AWS Lambda function that makes the API call.
2. Error Handling: Implement robust error handling to catch and report any issues during the payment process.
3. Success Completion: Publish a `charge-game-session-workflow.finished` event to `my-event-bus` upon successful charge.

### Example of events

Event Examples:

- **game-session.finished**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "gameDetails": {
      "duration": "<game_duration_in_minutes>",
      "cost": "<session_cost>"
    }
  }
}
```

- **charge-game-session-workflow.started**:

```json
{
  "source": "code-challenge",
  "detail-type": "charge-game-session-workflow.started",
  "detail": {
    "sessionId": "<unique_session_id>",
    "amount": "<charge_amount>"
  }
}
```

- **charge-game-session-workflow.failed**:

```json
{
  "source": "code-challenge",
  "detail-type": "charge-game-session-workflow.failed",
  "detail": {
    "sessionId": "<unique_session_id>",
    "error": "<error_message>"
  }
}
```

- **charge-game-session-workflow.finished**:

```json
{
  "source": "code-challenge",
  "detail-type": "charge-game-session-workflow.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "confirmation": "<payment_confirmation_code>"
  }
}
```

### Submission Guidelines
Adhere to the same submission guidelines as provided for the Code Challenge (A), with a focus on external API integration.

## Code Challenge (D) - Game Session Pause Handling

### Objective
Your task is to demonstrate handling game session status updates using AWS services. This includes interacting with Amazon S3 to update a game session's status to "Paused".

### Requirements
1. Infrastructure as Code: Employ IaC to provision AWS resources. Your code should be well-structured and follow best practices.
2. S3 and Lambda Integration: Set up an AWS Lambda function triggered by the `game-session-paused.requested` event on custom even bus named `my-event-bus`. The Lambda function should:
Update the status of the corresponding game session entry in an Amazon S3 bucket to Paused.
3. Error Handling: Ensure proper error handling to catch any issues during the status update process.
4. Success Completion: After successfully updating the game session status, publish a `game-session-paused.finished` event to `my-event-bus`.

### Example of events

- **game-session-paused.requested**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-paused.requested",
  "detail": {
    "sessionId": "<unique_session_id>"
  }
}
```

- **game-session-paused.updating**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-paused.updating",
  "detail": {
    "sessionId": "<unique_session_id>"
  }
}
```

- **game-session-paused.failed**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-paused.failed",
  "detail": {
    "sessionId": "<unique_session_id>",
    "error": "<error_message>"
  }
}
```

- **game-session-paused.finished**:

```json
{
  "source": "code-challenge",
  "detail-type": "game-session-paused.finished",
  "detail": {
    "sessionId": "<unique_session_id>",
    "status": "Paused"
  }
}
```

### Submission Guidelines
Adhere to the same submission guidelines as provided for the Code Challenge (A), focusing on demonstrating the ability to interact with Amazon S3 and process game session status updates efficiently.

---
Good luck, and we're looking forward to seeing your innovative solutions!
