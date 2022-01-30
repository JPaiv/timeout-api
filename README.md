# timeout_api
Timeout test 


## How it works

It will sort the incoming transactions based on latency time and then take the maximum value transactions under given latency time.

## Cloud solution

In actual practice we cannot know the latency times or trust them to stay reliable. That is why I made a serverless system on AWS using AWS Lambda, API Gateway and DynamoDb to process these transactions like they would work in actual production environment.


