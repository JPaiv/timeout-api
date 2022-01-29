package main

import (
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

// Response is of type APIGatewayProxyResponse since we're leveraging the
// AWS Lambda Proxy Request functionality (default behavior)
//
// https://serverless.com/framework/docs/providers/aws/events/apigateway/#lambda-proxy-integration
type Response events.APIGatewayProxyResponse

// Handler is our lambda handler invoked by the `lambda.Start` function call
func Handler(ctx context.Context, s3Event events.S3Event) {
	item := "api_latencies.json"
	file, err := os.Create(item)
	if err != nil {
		fmt.Println("Unable to open file %q, %v", item, err)
	}

	defer file.Close()

	for _, record := range s3Event.Records {
		s3 := record.S3
		fmt.Printf("[%s - %s] Bucket = %s, Key = %s \n", record.EventSource, record.EventTime, s3.Bucket.Name, s3.Object.Key)
	}
	sess, _ := session.NewSession(&aws.Config{Region: aws.String("us-east-1")})
	downloader := s3manager.NewDownloader(sess)
	numBytes, err := downloader.Download("api_latencies.json",
		&s3.GetObjectInput{
			Bucket: aws.String(s3.Bucket.Name),
			Key:    aws.String(s3.Object.Key),
		})
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Downloaded", file.Name(), numBytes, "bytes")
}

func main() {
	lambda.Start(Handler)
}
