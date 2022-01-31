# timeout_api
Timeout test 

## How it works

It will sort the incoming transactions based on latency time and then take the maximum value transactions under given latency time.

## Cloud solution

In actual practice we cannot know the latency times or trust them to stay reliable. That is why I made a serverless system on AWS using AWS Lambda, API Gateway and DynamoDb to process these transactions like they would work in actual production environment.

## Architecture

Using [serverless technologies](screenshot.png) it's possible to achive a reliable and secure transactions system. 

## Reasonings

### Why python?

I took production approach where I made a fast proof-of-concept to demonstrate. Python is an excellent tool for this type of scription. I didn't have to worry about Go build Makefiles and python ecosystem offers decent libraries for many troubles. Of course in actual production this would be written in Go.

### Why serverless?

Serverless framework is AWS CloudFormation as it should be. It removes boilerplate, is more intuitive and offers everything needed to run serverless application and their infra with one command. This spared me from having to work with containers and container orchestration. All services are serverless by nature.

## How to run

You can't, by definition serverless is used with event triggers. After deployment the user may place a source file into a bucket to trigger the process of transaction parse.

## CI/CD

Github Actions automates build, depency management and deployment. I wanted to showcase my skills in how I handle writing code, application and infrastrucsture deployment.

## But I don't want cloud!

Well there is the traditional no-cloud folder with a more traditional approach. 
