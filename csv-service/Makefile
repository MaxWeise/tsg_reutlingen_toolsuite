
APP_NAME := csv-service
IMG_NAME := tsg-reutlingen/$(APP_NAME)
IMG_TAG  := latest

.PHONY: all build run stop clean

all: build

build:
	@echo "Building Docker image $(IMG_NAME):$(IMG_TAG)..."
	docker build -t $(IMG_NAME):$(IMG_TAG) .
	@echo "Build complete."

run: build
	@echo "Running Docker container..."
	docker run --rm -p 7000:8080 --name $(APP_NAME)-container $(IMG_NAME):$(IMG_TAG)

test:
	@echo "Testing the package..."
	go test ./...

clean:
	@echo "Removing Docker image..."
	docker rmi $(IMG_NAME):$(IMG_TAG)
	@echo "Image removed."
