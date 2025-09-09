def call() {
sh '''
export PATH=$PATH:/usr/local/bin
echo "PATH is: $PATH"
which trivy
trivy --version
trivy image salmastudydocker/blog_web_app:latest
'''
}