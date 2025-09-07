def call() {
    echo "Building Docker image..."
    sh "docker build -t salmastudydocker/blog_web_app:latest -f ../../docker/blog/Dockerfile ../../docker/blog/"
    echo "Docker image built successfully!"
}
