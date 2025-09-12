def scanImage(String IMAGE_NAME) {
    if (!IMAGE_NAME || IMAGE_NAME == "null") {
        error("IMAGE_NAME is not set correctly. Please provide a valid image name.")
    }

    sh """
        docker run --rm \\
          -v /var/run/docker.sock:/var/run/docker.sock \\
          aquasec/trivy image ${IMAGE_NAME}
    """
}