def call(){
	echo "pushing docker image..."
	sh "docker push $IMAGE_NAME:${env.BUILD_NUMBER} "

}
