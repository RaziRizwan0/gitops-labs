<<<<<<< HEAD
# GitOps Labs

A portfolio-oriented GitOps delivery project using Flask, Docker, GitHub Actions, Kubernetes/Minikube, Kustomize, and Argo CD.

## Architecture

1. Push code to `dev`, `staging`, or `main`.
2. GitHub Actions runs unit tests.
3. The workflow builds and pushes an immutable Docker image tag.
4. The workflow updates the matching Kustomize overlay and commits the change.
5. Argo CD detects the Git change and reconciles Kubernetes.
6. Dev and staging sync automatically; production sync is manual.

## Naming

- GitHub repo: `gitops-labs`
- Docker Hub image: `YOUR_DOCKERHUB_USERNAME/gitops-labs`
- Namespaces: `gitops-dev`, `gitops-staging`, `gitops-production`
- Argo CD apps: `gitops-labs-dev`, `gitops-labs-staging`, `gitops-labs-production`

## 1. Verify prerequisites

```bash
docker --version
docker info
minikube version
kubectl version --client
git --version
```

Install missing `kubectl` using the official instructions: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

## 2. Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=6144 --disk-size=30g
kubectl config use-context minikube
kubectl get nodes
kubectl get pods -A
```

If your laptop has less memory, try `--cpus=2 --memory=4096` and avoid running extra monitoring components initially. Minikube's Docker driver docs: https://minikube.sigs.k8s.io/docs/drivers/docker/

## 3. Create repositories and secrets

Create a GitHub repository named `gitops-labs` and a Docker Hub repository also named `gitops-labs`. In GitHub repository Settings -> Secrets and variables -> Actions, add:

- `DOCKERHUB_USERNAME`: your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token with Read & Write permissions

Do not commit tokens or passwords.

## 4. Replace placeholders

Replace `YOUR_GITHUB_USERNAME` in `argocd/apps.yaml` with your actual GitHub username and `YOUR_DOCKERHUB_USERNAME` in each overlay with your actual Docker Hub username. For example, from the project root:

```bash
sed -i 's/YOUR_GITHUB_USERNAME/your-real-github-username/g' argocd/apps.yaml
sed -i 's/YOUR_DOCKERHUB_USERNAME/your-real-dockerhub-username/g' k8s/overlays/*/kustomization.yaml
```

Replace both example usernames before executing.

## 5. Push the project to GitHub

```bash
git init
git add .
git commit -m "feat: bootstrap GitOps Labs"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/gitops-labs.git
git push -u origin main
```

Use your actual repository URL. Create the environment branches from this starting point:

```bash
git checkout -b dev
git push -u origin dev
git checkout main
git checkout -b staging
git push -u origin staging
git checkout main
```

## 6. Push bootstrap image

The first deployment needs an image before the CI workflow has updated a tag. Log in interactively (never place a token in a command or source file):

```bash
docker login
docker build -t YOUR_DOCKERHUB_USERNAME/gitops-labs:bootstrap .
docker push YOUR_DOCKERHUB_USERNAME/gitops-labs:bootstrap
```

Use your actual Docker Hub username. Ensure all three overlays have the correct `newName` image reference.

## 7. Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=Available deployment --all -n argocd --timeout=300s
kubectl get pods -n argocd
```

Official getting started guide: https://argo-cd.readthedocs.io/en/stable/getting_started/

## 8. Open Argo CD UI

Run in one terminal and leave it running:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open `https://localhost:8080`. In a second terminal, get the initial password:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d; echo
```

Username is `admin`. Change the password after first login. Once changed, delete the initial secret:

```bash
kubectl delete secret argocd-initial-admin-secret -n argocd
```

Keep Argo CD local for this laptop project; do not expose it publicly without appropriate TLS and access controls.

## 9. Create Argo CD applications

After pushing `argocd/apps.yaml` to `main` and replacing the GitHub username:

```bash
kubectl apply -f argocd/apps.yaml
kubectl get applications -n argocd
```

Argo CD follows the same repo's branches: `dev` -> `gitops-dev`; `staging` -> `gitops-staging`; `main` -> `gitops-production`. Production has no automated sync policy, so use the Argo CD UI to manually sync `gitops-labs-production` after review.

## 10. Test CI/CD

```bash
git checkout dev
# Make a small edit in app.py
git add app.py
git commit -m "feat: improve app page"
git push
```

In GitHub -> Actions, verify tests pass, image is pushed, and the matching Kustomize overlay is committed. Argo CD should then deploy dev automatically. Repeat on `staging`; production requires a manual sync.

## 11. Verify and access the app

```bash
kubectl get applications -n argocd
kubectl get pods -n gitops-dev
kubectl get svc -n gitops-dev
kubectl port-forward -n gitops-dev svc/gitops-labs 8081:80
```

Open `http://localhost:8081`. Diagnostics:

```bash
kubectl describe deployment gitops-labs -n gitops-dev
kubectl logs deployment/gitops-labs -n gitops-dev
kubectl get events -n gitops-dev --sort-by=.lastTimestamp
```

## Portfolio extensions

Add Trivy image scanning, CodeQL/static analysis, Prometheus/Grafana metrics and alerts, encrypted secrets (SOPS or External Secrets), Kubernetes policy checks (Kyverno/OPA), rollback documentation, and an eventual PostgreSQL migration.

## Important limitations

This is a learning/portfolio project, not production-ready infrastructure. SQLite with one `ReadWriteOnce` PVC and one replica is intentionally simple; do not scale it to multiple replicas. Minikube is not highly available. Pin GitHub Actions to full commit SHAs and review permissions for stronger supply-chain security before calling this production-grade.
=======
# gitops-labs
>>>>>>> 3399afc1d30d64e1b52faffabc77fc0b321498f1
