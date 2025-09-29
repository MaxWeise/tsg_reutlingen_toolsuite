FROM golang:latest

WORKDIR /usr/bin/app

COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
RUN go build -v -o /usr/local/bin/app

# Map 7000 external Port to 8080 internal Port
EXPOSE 7000

# The command to run when the container starts
CMD ["app"]
