def call() {
    echo "Building Docker image..."
    sh "docker build -t $IMAGE_NAME -f docker/blog/Dockerfile docker/blog"
    echo "Docker image built successfully!"
}
