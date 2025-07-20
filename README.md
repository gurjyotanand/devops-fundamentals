# DevOps Fundamentals and Getting Started with Simple CI/CD Pipeline Implementation

Modern software development requires seamless integration between development and operations teams to deliver high-quality applications efficiently. This guide explores DevOps principles and demonstrates practical CI/CD pipeline implementation using industry-standard tools.

## What You'll Learn

- Core DevOps principles and their business impact
- DevOps lifecycle phases and tool integration
- Practical CI/CD pipeline implementation with Jenkins and Docker
- Industry best practices for automated deployment workflows

## Understanding DevOps: Beyond the Buzzword

DevOps represents a cultural and technical transformation that bridges the traditional gap between software development and IT operations. This methodology emphasizes **collaboration**, **automation**, and **continuous improvement** as fundamental pillars for modern software delivery.

**[Image Placeholder]**: *Suggest: DevOps culture transformation diagram showing the evolution from siloed teams to collaborative cross-functional units with shared responsibilities*

The core philosophy transforms isolated departmental structures into unified, cross-functional teams that share responsibility for the entire software lifecycle. This paradigm shift eliminates traditional bottlenecks and accelerates delivery cycles while maintaining system reliability.

## DevOps Lifecycle Architecture

The DevOps workflow operates as a continuous cycle encompassing eight interconnected phases: **Plan**, **Develop**, **Build**, **Test**, **Release**, **Deploy**, **Operate**, and **Monitor**. Each phase seamlessly transitions into the next, creating an infinite loop of improvement and delivery.

**[Image Placeholder]**: *Suggest: Circular DevOps lifecycle diagram with arrows showing the continuous flow between Plan → Develop → Build → Test → Release → Deploy → Operate → Monitor → Plan*

### Tool Ecosystem Integration

Each lifecycle phase leverages specialized tools optimized for specific functions:

| Phase | Primary Tools | Function |
|-------|---------------|----------|
| **Plan** | Jira, Git | Project management and version control |
| **Build/Test** | Jenkins, Bamboo, Maven | Continuous integration and testing |
| **Deploy** | Docker, Kubernetes, Helm | Container orchestration and deployment |
| **Monitor** | Prometheus, Grafana | Performance monitoring and observability |

## Traditional IT vs DevOps: A Comparative Analysis

The transformation from traditional IT practices to DevOps methodology represents a fundamental shift in organizational approach:

| Characteristic | Traditional IT | DevOps Implementation |
|----------------|----------------|----------------------|
| **Team Structure** | Departmental silos | Cross-functional collaboration |
| **Delivery Process** | Manual, sequential | Automated, parallel |
| **Failure Management** | Reactive, concealed | Proactive, transparent |
| **Tool Integration** | Isolated, manual processes | Unified CI/CD pipelines |

This transformation significantly reduces deployment risks, accelerates time-to-market, and improves system reliability through automated testing and monitoring.

## Production Workflow Example

Consider a modern DevOps implementation: A developer commits Python code to GitHub, which automatically triggers Jenkins to initiate the build process. Docker containerizes the application, Kubernetes orchestrates the deployment, MLflow tracks model performance metrics, and Prometheus provides real-time monitoring across the entire infrastructure.

**[Image Placeholder]**: *Suggest: End-to-end workflow diagram showing code commit → Jenkins trigger → Docker build → Kubernetes deployment → MLflow tracking → Prometheus monitoring with connecting arrows and tool logos*

This automated workflow eliminates manual intervention, reduces human error, and ensures consistent deployment practices across environments.

## Essential DevOps Toolchain for 2025

Professional DevOps implementations rely on a curated set of tools, each optimized for specific operational requirements:

| Function Category | Recommended Tools | Purpose |
|-------------------|------------------|---------|
| **CI/CD Automation** | Jenkins, GitHub Actions, GitLab | Build and deployment orchestration |
| **Containerization** | Docker | Application packaging and isolation |
| **Container Orchestration** | Kubernetes | Production-scale container management |
| **Infrastructure as Code** | Terraform | Declarative infrastructure provisioning |
| **Monitoring & Observability** | Prometheus, Grafana, ELK  | System metrics and visualization |
| **Source Code Management** | Bitbucket, Git | Version control and collaboration |

## Career Opportunities in DevOps

The DevOps field presents significant professional opportunities with high market demand across industries. Primary career paths include **DevOps Engineer**, **Platform Engineer**, and **Site Reliability Engineer (SRE)** roles, each offering competitive compensation packages and substantial career growth potential.

**[Image Placeholder]**: *Suggest: Career progression chart showing entry-level to senior DevOps roles with salary ranges and required skills for each level*

Organizations increasingly prioritize DevOps expertise as digital transformation initiatives expand, creating sustained demand for qualified professionals.

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

# Create subdirectories for different components
mkdir -p {jenkins,k8s-manifests,helm-charts,monitoring,apps}

# Create initial directory structure
tree . # or use ls -la if tree is not installed
```

---

## Jenkins, Docker, Kubernetes, Helm Setup

**Step 1: Deploy Jenkins using Docker**

First, let's create a custom Jenkins Docker setup:

```bash
cd ~/devops-simple-ci-cd-pipelinejenkins

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