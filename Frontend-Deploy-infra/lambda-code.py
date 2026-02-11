import json
import boto3

# Initialize the SageMaker runtime client
runtime = boto3.client('sagemaker-runtime')

# Replace this with your actual endpoint name
ENDPOINT_NAME = 'hyd-house-endpoint-rajini'

def lambda_handler(event, context):
    try:
        # 1. Parse data from the UI (API Gateway passes it as a string in 'body')
        body = json.loads(event['body'])
        # Extract features list (e.g., [2500, 3, 2, 1])
        features = body['features'] 
        
        # 2. Format for SageMaker (it expects CSV or JSON string)
        payload = ",".join(map(str, features))
        
        # 3. Call SageMaker Endpoint
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='text/csv',
            Body=payload
        )
        
        # 4. Decode the result
        result = json.loads(response['Body'].read().decode())
        
        # 5. Return to UI with CORS headers enabled
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*', # Allows local UI to call API
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'prediction': result[0]})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
