def call() {
    echo "Scanning Docker image..."
    sh "/snap/bin/trivy image ${IMAGE_NAME}"
}
