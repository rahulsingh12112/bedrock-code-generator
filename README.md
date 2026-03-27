# AWS Bedrock Code Generator

 Serverless application that generates code using Amazon Bedrock and stores it in S3.

## Architecture

User Request → API Gateway → Lambda → Bedrock (Claude) → S3 Storage

## Features

- ✅ REST API endpoint for code generation
- ✅ Multiple programming languages support (Python, Java, JavaScript, etc.)
- ✅ Automatic S3 storage with timestamps
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive error handling

## Tech Stack

- **AWS Lambda** - Python 3.12 runtime
- **Amazon Bedrock** - Claude Sonnet 4.6 model
- **Amazon S3** - Code storage
- **Amazon API Gateway** - REST API endpoint
- **AWS IAM** - Security & permissions

## API Usage

**Endpoint:** `POST /generate-code`

**Request Body:**
```json
{
  "instruction": "Create a function to reverse a string",
  "programming_language": "Python"
}
Response:

json

{
  "message": "Code generated successfully",
  "programming_language": "Python",
  "s3_bucket": "bedrock-generated-code-bucket",
  "s3_key": "generated-code/Python/20260327_082700.py",
  "generated_code": "# Generated code here..."
}

Supported Languages
Python | Java | JavaScript | TypeScript | Go | Ruby | C++ | C# | PHP | Swift

Setup Instructions
Prerequisites
AWS Account with Bedrock access
IAM permissions for Lambda, Bedrock, S3, API Gateway
Deployment Steps
Create S3 Bucket

Bucket name: bedrock-generated-code-bucket-<your-name>
Region: us-east-1
Create IAM Role

Attach AWSLambdaBasicExecutionRole
Add custom policy for Bedrock & S3 access
Deploy Lambda Function

Runtime: Python 3.12
Timeout: 60 seconds
Memory: 512 MB
Environment variable: S3_BUCKET_NAME
Create API Gateway

REST API with /generate-code resource
POST method with Lambda proxy integration
Deploy to prod stage
Project Highlights
Serverless Architecture - No server management
Cost-Effective - Pay only for what you use
Scalable - Auto-scales with demand
Secure - IAM-based access control
Production-Ready - Error handling & logging
Cost Estimate
API Gateway: ~$3.50 per million requests
Lambda: ~$0.20 per 1M requests
Bedrock: ~$0.003 per 1K tokens
S3: ~$0.023 per GB
Estimated monthly cost for 1000 requests: $2-5

Author
Rahul - AWS Solutions Architect

License
MIT License


**3. `docs/architecture.md`** - Architecture details:

```markdown
# Architecture Documentation

## System Flow

1. **User Request** → API Gateway receives POST request
2. **API Gateway** → Triggers Lambda function
3. **Lambda** → Parses request body
4. **Lambda** → Calls Bedrock API with instruction
5. **Bedrock** → Generates code using Claude model
6. **Lambda** → Saves code to S3 with timestamp
7. **Lambda** → Returns response with S3 location

## Components

### API Gateway
- REST API endpoint
- CORS enabled
- Lambda proxy integration

### Lambda Function
- Python 3.12 runtime
- 512 MB memory
- 60 seconds timeout
- Environment variables for S3 bucket

### Amazon Bedrock
- Model: Claude Sonnet 4.6
- Max tokens: 4096
- Temperature: 0.7

### S3 Storage
- Organized by programming language
- Timestamped filenames
- Metadata tags

## Security

- IAM role-based access
- Least privilege principle
- No public S3 access
- API Gateway authentication ready

