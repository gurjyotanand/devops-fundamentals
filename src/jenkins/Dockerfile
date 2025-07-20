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
