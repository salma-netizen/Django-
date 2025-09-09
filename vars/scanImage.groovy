def call(String IMAGE_NAME) {
    sh """
        /usr/local/bin/trivy --version
       /usr/local/bin/trivy image ${IMAGE_NAME}
    """
}