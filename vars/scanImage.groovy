def call() {
    echo "Scanning Docker image..."
    sh "trivy image $IMAGE_NAME"
}