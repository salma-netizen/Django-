def call() {
    echo "Scanning Docker image..."
    sh '/home/ubuntu/bin/trivy image ${IMAGE_NAME}'
}
