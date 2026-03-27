import json
import boto3
from datetime import datetime
import os
# Initialize AWS clients
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
# S3 bucket name from environment variable
S3_BUCKET = os.environ.get('S3_BUCKET_NAME', 'bedrock-generated-code-bucket-1212112')
def lambda_handler(event, context):
    """
    Main Lambda handler function
    """
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        # Extract parameters
        instruction = body.get('instruction')
        programming_language = body.get('programming_language', 'Python')
        # Validation
        if not instruction:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'instruction parameter is required'
                })
            }
        # Step 1: Generate code using Bedrock
        print(f"Generating {programming_language} code for: {instruction}")
        generated_code = generate_code_with_bedrock(instruction, programming_language)
        if not generated_code:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Failed to generate code from Bedrock'
                })
            }
        # Step 2: Save to S3
        s3_key = save_to_s3(generated_code, programming_language)
        if not s3_key:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Failed to save code to S3'
                })
            }
        # Success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Code generated successfully',
                'programming_language': programming_language,
                'instruction': instruction,
                's3_bucket': S3_BUCKET,
                's3_key': s3_key,
                's3_url': f"s3://{S3_BUCKET}/{s3_key}",
                'generated_code': generated_code
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
 
def generate_code_with_bedrock(instruction, programming_language):
    """
    Bedrock model ko call karke code generate karta hai
    """
    prompt = f"""You are an expert programmer. Generate clean, well-documented code based on the following requirements:
Programming Language: {programming_language}
Task: {instruction}
Please provide only the code with appropriate comments. Do not include explanations outside the code."""
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    try:
        # Using Global CRIS profile for Claude Sonnet 4.6
        response = bedrock_runtime.invoke_model(
            modelId='global.anthropic.claude-sonnet-4-6',
            body=json.dumps(request_body)
        )
        # Parse response
        response_body = json.loads(response['body'].read())
        # FIX: content is a LIST - access first element with [0] then get "text"
        generated_code = response_body['content'][0]["text"]
        print(f"Successfully generated code: {len(generated_code)} characters")
        return generated_code
    except Exception as e:
        print(f"Bedrock error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None
 
def save_to_s3(code_content, programming_language):
    """
    Generated code ko S3 mein save karta hai
    """
    extensions = {
        'Python': '.py',
        'Java': '.java',
        'JavaScript': '.js',
        'TypeScript': '.ts',
        'Go': '.go',
        'Ruby': '.rb',
        'C++': '.cpp',
        'C#': '.cs',
        'PHP': '.php',
        'Swift': '.swift'
    }
    extension = extensions.get(programming_language, '.txt')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    s3_key = f"generated-code/{programming_language}/{timestamp}{extension}"
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=code_content.encode('utf-8'),
            ContentType='text/plain',
            Metadata={
                'programming-language': programming_language,
                'generated-at': timestamp
            }
        )
        print(f"Code saved to S3: s3://{S3_BUCKET}/{s3_key}")
        return s3_key
    except Exception as e:
        print(f"S3 error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None
