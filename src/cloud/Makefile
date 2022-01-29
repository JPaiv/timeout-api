.PHONY: build clean deploy

build:
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o ./hello hello/main.go
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o ./world world/main.go

clean:
	rm -rf ./bin

deploy: clean build
	sls deploy --verbose
