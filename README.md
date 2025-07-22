# Getting Started with Simple CI/CD Pipeline Implementation

Modern software development requires seamless integration between development and operations teams to deliver high-quality applications efficiently. This guide explores DevOps principles and demonstrates practical CI/CD pipeline implementation using industry-standard tools.

## What You'll Learn

- Core DevOps principles and their business impact
- DevOps lifecycle phases and tool integration
- Practical CI/CD pipeline implementation with Jenkins and Docker
- Industry best practices for automated deployment workflows


## Prerequisites

Before we begin, ensure you have the following installed on your Mac:

1. **Homebrew** (package manager for macOS)
2. **OrbStack** (modern Docker alternative)
3. **Git** (version control)
4. **kubectl** (Kubernetes CLI)
5. **Helm** (Kubernetes package manager)

**Step 1: Install Required Tools**

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install OrbStack
brew install --cask orbstack

# Install Git (usually pre-installed on Mac)
brew install git

# Install kubectl (Kubernetes CLI)
brew install kubectl

# Install Helm
brew install helm

```

**Step 2: Verify OrbStack Installation**

```bash
# Start OrbStack (it should start automatically after installation)
# Check if Docker is working through OrbStack
docker --version
docker run hello-world

# Verify Kubernetes is enabled in OrbStack
kubectl cluster-info
kubectl get nodes
```

**Step 3: Create Project Structure**

```bash
# Create main project directory
mkdir ~/devops-simple-ci-cd-pipeline
cd ~/devops-simple-ci-cd-pipeline

# Initialize git repo
git init

# Create src/ folder
mkdir src

# Change directory to src/ folder
cd src
```

**Step 4: Create app.py in src/ Directory**

```bash
cat > app.py << 'EOF'
from flask import Flask

# Create a Flask web server
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello, World from Kubernetes and Helm!\n'

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to be publicly accessible from within the container
    app.run(host='0.0.0.0', port=2867)
EOF
```
---

## Installations

**Step 1: Deploy Jenkins using Docker**

First, let's create a custom Jenkins Docker setup:

```bash
mkdir jenkins
cd ~/jenkins

# Create Jenkins Dockerfile for custom setup
cat > Dockerfile << 'EOF'
FROM jenkins/jenkins:lts

# Switch to root to install additional tools
USER root

# Install basic utilities and Docker CLI
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (architecture-aware)
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl (architecture-aware)
RUN ARCH=$(dpkg --print-architecture) \
    && if [ "$ARCH" = "amd64" ]; then KUBECTL_ARCH="amd64"; else KUBECTL_ARCH="arm64"; fi \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${KUBECTL_ARCH}/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add jenkins user to docker group (create group if it doesn't exist)
RUN groupadd -f docker && usermod -aG docker jenkins

# Switch back to jenkins user
USER jenkins

EOF

# Build custom Jenkins image
docker build -t custom-jenkins:latest .
```

**Step 2: Create Jenkins Docker Compose**

```bash
# Create docker-compose.yml for Jenkins
cat > docker-compose.yml << 'EOF'
services:
  jenkins:
    build: .
    container_name: jenkins
    restart: unless-stopped
    user: root  # Run as root to avoid permission issues
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/.kube:/var/jenkins_home/.kube:ro
    environment:
      - DOCKER_HOST=unix:///var/run/docker.sock
      - JENKINS_USER=jenkins
    networks:
      - jenkins-network

volumes:
  jenkins_home:
    name: main_jenkins_home

networks:
  jenkins-network:
    driver: bridge

EOF
```

## Start Jenkins and get Jenkins Admin password
```
docker-compose up -d
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 
```

Note: After this push your files to your github repository. 