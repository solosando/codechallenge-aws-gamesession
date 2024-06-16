# Code Challenge (A) Solution

## Deploying Solution:

To run this code, you need to have Python and the AWS CLI installed on your machine, along with the virtual environment package. You can install them using pip 16.7.9 or higher.
For this cloudformation, you`ll need permissions to create IAM rules and assuming roles.

To run the code, follow these steps:

1. Clone this repository .
2. Create a virtual environment using Virtualenv and activate it:

   `python -m venv .venv`
   `. .venv/bin/activate`

3. Install dependencies in your virtual environment by running the following commands inside the virtual environment:

   `python -m pip install boto3`

4. Set up AWS credentials as per the instructions [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation).

5. Run the command to deploy the stack specifying the arguments: 

   - --bucket-name=The name of the s3 bucket to be created
   - --file-name = The path to the directory containing the .zip file with lambda code
   - --stack-name =The name of the cloudformation stack to be created
   - --template-body=The yaml file with the stack resources to be crated
   - --capabilities=The capabilities for the cloudformation stack
   - --parameters=The parameters for the cloudformation stack
   - --events-dir =The path to the directory containing the JSON files with event details

 Example: 

  `python3 cfn_utils.py --bucket-name code-challenge-2024-03-lambda --file-name lambda_function.py.zip --stack-name codechallengestack --template-body file://template.yaml --capabilities CAPABILITY_NAMED_IAM --table-name mytable --event-bus-name my-event-bus --events-dir events`

