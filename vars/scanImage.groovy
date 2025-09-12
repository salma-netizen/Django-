def call(String imageName) {
    if (!imageName || imageName == "null") {
        error("IMAGE_NAME is not set correctly.")
    }

    sh """
        docker run --rm \\
          -v /var/run/docker.sock:/var/run/docker.sock \\
          aquasec/trivy image ${imageName}
    """
}