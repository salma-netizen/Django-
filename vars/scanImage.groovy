def call(){
	echo "scanning docker image..."
	sh "trivy image $IMAGE_NAME:${env.BUILD_NUMBER} "

}
