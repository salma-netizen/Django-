def call(String IMAGE_NAME) {
    sh """
       sudo  /usr/local/bin/trivy --version
       sudo /usr/local/bin/trivy image ${IMAGE_NAME}
    """
}