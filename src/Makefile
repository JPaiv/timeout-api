.PHONY: build clean deploy

build:
	go get -u github.com/aws/aws-lambda-go/lambda
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o bin/latency-data latency-data/main.go
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o bin/verification-api verification-api/main.go

clean:
	rm -rf ./bin

deploy: clean build
	sls deploy --verbose
