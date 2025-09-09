echo "scanning docker image..."
sh '''
export PATH=$PATH:/home/ubuntu/bin
trivy image salmastudydocker/blog_web_app:latest
'''
