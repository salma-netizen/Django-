def call() {
    echo "Building Docker image..."
    sh "docker build -t $IMAGE_NAME  ../../docker/blog/Dockerfile"
    echo "Docker image built successfully!"
}
