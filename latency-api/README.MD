# Cloud timeout api

Purpose was to show how a timeout api would function in a simulation environment.

## Process

1. Place json latency data file to source bucket to trigger create-latency-table.py-lambda which creates dynamo database items for the latency api.

2. Trigger the process by placing transaction.csv to bucket to trigger verification-api

3. Latency-api will then make queries based on HTTP get from verification-api

4. Return as many as possible before time(1 minutes) runs out

5. Send unused transaction to SQS Queue to wait for a better time for verification

## Purpose 

Purpose was to show my skills in software engineering, architecture design, DevOps engineering. 

Cloud: AWS Api Gateway, Lambda, S3, DynamoDb
CI/CD: Github Actions
IaC: Serverless framework
