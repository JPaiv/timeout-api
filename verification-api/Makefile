.PHONY: build clean deploy

build:
	go get -u github.com/aws/aws-lambda-go/lambda
	go get -u github.com/aws/aws-sdk-go/aws
	go get -u github.com/aws/aws-sdk-go/aws/session
	go get -u github.com/aws/aws-sdk-go/service/s3
	go get -u github.com/aws/aws-sdk-go/service/s3/s3manager
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o bin/verification-api verification-api/main.go

clean:
	rm -rf ./bin

deploy: clean build
	sls deploy --verbose
