def call() {
    echo "📦 Pushing updated Kubernetes manifests to GitHub repository..."

    withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
        sh 'git config user.name "salma-netizen"'
        sh 'git config user.email "engsalmaelsayed7@gmail.com"'

        // Set remote URL with embedded credentials
        sh 'git remote add origin https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/salma-netizen/Django-.git'

        // Ensure you're on a valid branch
        sh 'git checkout -B main'

        // Add and commit only if there are changes
        sh """
            git add k8s/deployment-djanjo.yml
            git diff --cached --quiet || git commit -m "Update Kubernetes deployment manifest with new image tag"
        """

        // Push to GitHub
        sh 'git push origin main'
    }

    echo "✅ Manifests have been successfully pushed to GitHub."
}
