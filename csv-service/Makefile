# Makefile for the csv-service

# --- Variables ---
# Use a variable for the application name to avoid repetition.
APP_NAME := csv-service
# Define the Docker image name and tag.
IMG_NAME := tsg-reutlingen/$(APP_NAME)
IMG_TAG  := latest

# --- Docker Targets ---

# The .PHONY directive tells make that these are not files.
.PHONY: all build run stop clean

# Default target: running `make` will be the same as `make all`
all: build

# Build the Docker image
# `docker build` command reads the Dockerfile from the current directory (`.`).
# `-t` tags the image with a name and tag for easy reference.
build:
	@echo "Building Docker image $(IMG_NAME):$(IMG_TAG)..."
	docker build -t $(IMG_NAME):$(IMG_TAG) .
	@echo "Build complete."

# Run the Docker container
# This target depends on `build`, so it will build the image first if it doesn't exist.
# `-p 7000:7000` maps port 7000 on the host to port 7000 in the container.
# `--rm` automatically removes the container when it stops.
# `--name` gives the running container a predictable name for easy management (e.g., for stopping it).
run: build
	@echo "Running Docker container..."
	docker run --rm -p 7000:8080 --name $(APP_NAME)-container $(IMG_NAME):$(IMG_TAG)

test:
	@echo "Testing the package..."
	go test ./...

# Clean up by removing the Docker image
# `docker rmi` removes the specified image.
clean:
	@echo "Removing Docker image..."
	docker rmi $(IMG_NAME):$(IMG_TAG)
	@echo "Image removed."
