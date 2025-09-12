// vars/pushManifests.groovy
def call() {
    echo "Pushing updated Kubernetes manifests to GitHub repository..."

    sh 'git config --global user.name "Jenkins"'
    sh 'git config --global user.email "jenkins@example.com"'

    sh 'git add k8s/deployment-djanjo.yml'

    sh 'git commit -m "Update..." || echo "No changes to commit."'

    sh 'git push origin main'

    echo "Manifests have been successfully pushed to GitHub."
}
