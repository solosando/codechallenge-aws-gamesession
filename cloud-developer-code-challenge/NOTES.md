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

   --bucket-name=The name of the s3 bucket to be created
   --file-name = The path to the directory containing the .zip file with lambda code
   --stack-name =The name of the cloudformation stack to be created
   --template-body=The yaml file with the stack resources to be crated
   --capabilities=The capabilities for the cloudformation stack
   --parameters=The parameters for the cloudformation stack
   --events-dir =The path to the directory containing the JSON files with event details

 Example: 

  `python3 cfn_utils.py --bucket-name code-challenge-2024-03-lambda --file-name lambda_function.py.zip --stack-name codechallengestack --template-body file://template.yaml --capabilities CAPABILITY_NAMED_IAM --table-name mytable --event-bus-name my-event-bus --events-dir events`


## Testing: 
Due to the components, the best test approach is thest them sepparately.

### Testing the lambda function
To test the lambda function, you can create a test table at DynamoDb using CLI command: 

  ' aws dynamodb create-table \
    --table-name Test \         
    --attribute-definitions \
        AttributeName=Test,AttributeType=S \
    --key-schema AttributeName=Test,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1 '
When the test table is created, the output should look like this:

To invoke lambda function, execute the following:
 
 ' aws lambda invoke \
    --function-name FunctionName \
    --payload file://test-event.json \
    --payload-format json \
    output.json \
    --region us-east-1 \
    --profile your-profile-name \
    --invocation-type RequestResponse \
    --role your-role-arn '

Your output should look like this:

Now that the lambda is working propperly, the cfn_utils  module will be tested.

### Test for cfn_utils
Install pytest and pytest-mock for testing:

`pip install pytest pytest-mock`
Then run `pytest` on the directory of cfn_utils

### Application test
After deployed, verify  that your application is working correctly by running the below test.
