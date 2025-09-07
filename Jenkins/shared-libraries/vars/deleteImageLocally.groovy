def call(){
	echo "delete image locally..."
	sh "docker rmi $IMAGE_NAME:${env.BUILD_NUMBER} "

}
