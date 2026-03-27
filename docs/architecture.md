
# Architecture Documentation

bedrock-code-generator/
│
├── README.md
├── .gitignore
├── architecture-diagram.png
│
├── lambda/
│   ├── lambda_function.py
│   ├── requirements.txt
│   └── README.md
│
├── api-gateway/
│   ├── api-definition.json
│   └── README.md
│
├── iam-policies/
│   ├── lambda-execution-role.json
│   └── README.md
│
├── test/
│   ├── sample-requests.json
│   └── test-api.sh
│
└── docs/
    ├── setup-guide.md
    └── api-documentation.md

## Data Flow

1. **User Request** → API Gateway receives POST request with instruction and programming language
2. **API Gateway** → Triggers Lambda function with event payload
3. **Lambda Handler** → Parses request body and extracts parameters
4. **Bedrock Call** → Lambda calls Bedrock API with prompt
5. **Code Generation** → Claude model generates code based on instruction
6. **S3 Storage** → Lambda saves generated code to S3 with timestamp
7. **Response** → Lambda returns success response with S3 location and generated code

## Security

- **IAM Role-Based Access** - Lambda execution role with least privilege
- **Bedrock Permissions** - `bedrock:InvokeModel` only
- **S3 Permissions** - `s3:PutObject` only on specific bucket
- **No Public Access** - S3 bucket blocks all public access
- **CORS Enabled** - API Gateway allows frontend integration

## Cost Optimization

- **Serverless Architecture** - No idle costs
- **Lambda Memory** - Optimized at 512 MB
- **S3 Lifecycle** - Can add policies to archive old files
- **Bedrock On-Demand** - Pay per token usage
