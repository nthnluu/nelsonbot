# bots at brown

## Bot-specific events

### Nelson Bot
```json
{
    "botType": "nelson",
    "username": "YOUR BROWN USERNAME",
    "password": "YOUR BROWN PASSWORD",
    "duoBypass": "A DUO BYPASS CODE",
    "refreshCount": 300,  // optional, the number of times to retry.
    "refreshInterval": 2  // optional, number of seconds to wait between retries
}
```

## Commands

Run these commands in sequence:

`make lambda-layer-build` to prepare archive for AWS Lambda Layer deploy (layer.zip)

`make lambda-function-build` to prepare archive for AWS Lambda deploy (deploy.zip)

`make BUCKET=<your_bucket_name> create-stack` to create CloudFormation stack (lambda function, layer and IAM role)

## Offline execution (using Docker)

`make docker-build` to prepare Docker image for AWS Lambda offline execution  

`make lambda-run` to execute AWS Lambda in Docker
