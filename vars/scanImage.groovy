def call(){
	echo "scanning docker image..."
	sh "sh '/snap/bin/trivy image $IMAGE_NAME' "

}
