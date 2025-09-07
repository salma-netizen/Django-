def call(){
	echo "delete image locally..."
	sh "docker rmi $IMAGE_NAME"

}
