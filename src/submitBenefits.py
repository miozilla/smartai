import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Extract Bedrock agent information
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    print(parameters)
    try:
        # Extract parameters from the Bedrock agent input
        policy_number = next((p['value'] for p in parameters if p['name'] == 'policy_number'), None)
        claim_type = next((p['value'] for p in parameters if p['name'] == 'claim_type'), None)
        claim_amount = next((p['value'] for p in parameters if p['name'] == 'claim_amount'), None)
        member_id = next((p['value'] for p in parameters if p['name'] == 'member_id'), None)
        
        # Validate required fields
        if not all([policy_number, claim_type, claim_amount, member_id]):
            responseBody = {
                "TEXT": {
                    "body": "Error: Missing required parameters for insurance claim submission"
                }
            }
        else:
            # Create a unique claim ID
            claim_id = f"CLM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create claim data
            claim_data = {
                'claim_id': claim_id,
                'policy_number': policy_number,
                'claim_type': claim_type,
                'claim_amount': claim_amount,
                'member_id': member_id,
                'submission_date': datetime.now().isoformat(),
                'status': 'SUBMITTED'
            }
            
            # Here you would add your database interaction code
            # Example: Save to DynamoDB, RDS, etc.
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('BenefitsTable')
            table.put_item(
                Item=claim_data
            )
            
            responseBody = {
                "TEXT": {
                    "body": f"Claim submitted successfully! Claim ID: {claim_id}"
                }
            }
            
    except Exception as e:
        responseBody = {
            "TEXT": {
                "body": f"Error processing claim: {str(e)}"
            }
        }
    
    # Construct the response in the required Bedrock agent format
    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }
    
    # Final response structure
    final_response = {
        'response': action_response,
        'messageVersion': event['messageVersion']
    }
    
    print("Response: {}".format(final_response))
    return final_response