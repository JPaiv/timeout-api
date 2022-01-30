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
func handler(ctx context.Context, s3Event events.S3Event) {
	fmt.Printf("File: %s", s3Event)
	for _, record := range s3Event.Records {
		s3 := record.S3
		fmt.Printf("[%s - %s] Bucket = %s, Key = %s \n", record.EventSource, record.EventTime, s3.Bucket.Name, s3.Object.Key)
	}
	file, err := os.Create(s3.Object.Key)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()

	sess, _ := session.NewSession(&aws.Config{Region: aws.String("eu-west-1")})
	downloader := s3manager.NewDownloader(sess)
	numBytes, err := downloader.Download(file,
		&s3.GetObjectInput{
			Bucket: aws.String(s3.Bucket.Name),
			Key:    aws.String(s3.Object.Key),
		})
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("File: %s", numBytes)

}

func main() {
	lambda.Start(handler)
}
