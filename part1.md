# Practical Implementation: Jenkins CI/CD Pipeline with Docker Compose

This section demonstrates hands-on implementation of a production-ready CI/CD pipeline using Jenkins and Docker Compose. The following tutorial establishes automated build and deployment workflows that mirror enterprise-level practices.

One you have completed the steps in the README.md file and jenkins container is running, Access the Jenkins interface at `http://localhost:8080`.

![Jenkins Initial Setup Screen](images/part1-b-1.png)

Input the admin password into the Jenkins setup interface to proceed with configuration.

![CLI](images/part1-b-2.png)

### Plugin Installation

Jenkins requires specific plugins for Git integration and pipeline functionality:

- **Git Plugin**: Enables repository connectivity
- **Pipeline Plugin**: Supports pipeline-as-code workflows  
- **Docker Pipeline Plugin**: Facilitates container integration (optional)

Complete the plugin installation and create an administrative user account.

### Project Configuration

Create a new Freestyle project with the following specifications:

1. Navigate to "New Item" in the Jenkins dashboard
2. Enter project name: `ci-demo`
3. Select "Freestyle project" template
4. Configure Source Code Management with Git
5. Specify your GitHub repository URL
6. Change branch to `*/main`

![Jenkins Pipeline Setup-1](images/part1-b-3.png)

![Jenkins Pipeline Setup-2](images/part1-b-4.png)

### Build Step Configuration

Add an execution shell build step with basic commands:

```bash
echo "Initiating application build process..."
```

**[Image Placeholder]**: *Suggest: Jenkins project configuration screen showing the build steps section with shell command input field*

### Webhook Integration (Optional)

For automated build triggers, configure GitHub webhooks:

1. Access GitHub repository settings
2. Navigate to Webhooks section
3. Set payload URL: `http://:8080/github-webhook/`
4. Configure content type as `application/json`

### Pipeline Testing

Validate the implementation by pushing code to your GitHub repository. Jenkins should automatically detect the change and execute the build process.

![Successful Pipeline Run](images/part1-b-5.png)

## Troubleshooting Common Issues

| Problem | Resolution |
|---------|-----------|
| **Port 8080 occupied** | Modify port mapping in `docker-compose.yml` |
| **Repository cloning failure** | Verify repository accessibility or configure authentication |
| **Jenkins startup issues** | Execute `docker logs jenkins-ci` for diagnostic information |

## What's Next?

The next phase of implementation will integrate Docker image building and container registry management into the Jenkins pipeline, creating a complete containerized deployment workflow for modern application delivery and deploying 
