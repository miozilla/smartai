import json
import boto3

def lambda_handler(event, context):
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    print(parameters)

    # Execute your business logic here. For more information, refer to: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VacationTable')
    
    # Initialize variables
    employee_name = None
    startDate = None
    endDate = None
    
    # Check parameters and assign values
    for param in parameters:
        if param.get('name') == 'employee_name':
            employee_name = param['value']
        elif param.get('name') == 'startDate':
            startDate = param['value']
        elif param.get('name') == 'endDate':
            endDate = param['value']

    # insert the row
    table.put_item(
        Item={
            'employee_name': employee_name,
            'startDate': startDate,
            'endDate': endDate
        }
    )

    responseBody =  {
        "TEXT": {
            "body": "The function {} was called successfully!".format(function)
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    dummy_function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response


