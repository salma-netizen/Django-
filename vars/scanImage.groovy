def call(String IMAGE_NAME) {
    sh """
        docker run --rm \\
          -v /var/run/docker.sock:/var/run/docker.sock \\
          aquasec/trivy image ${IMAGE_NAME}
    """
}