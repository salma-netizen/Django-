def call() {
    echo "📦 Pushing updated Kubernetes manifests to GitHub repository..."

    sh 'git config user.name "Jenkins"'
    sh 'git config user.email "jenkins@example.com"'

    // Ensure we're on the correct branch
    sh 'git checkout -B main'

    // Add and commit only if there are changes
    sh """
        git add k8s/deployment-djanjo.yml
        git diff --cached --quiet || git commit -m "Update Kubernetes deployment manifest with new image tag"
    """

    // Push to GitHub
    sh 'git push origin main'

    echo "✅ Manifests have been successfully pushed to GitHub."
}
