# Introduction

This guide is written to provide a basic working example for a sample .NET Core application in ECS Fargate. 

## Requirements

There are a number of requirements that shoul be met before getting started:

* An AWS account
* A Splunk Infrastructure Monitor & APM account
* Mac OS latest version (or) Windows 10 with latest updates (or) Ubuntu 18.0.4 or higher. Note -- if desired, cleanup following this example may be easier if ran on an Ubuntu VM.
* [.NET Core 3.0](https://dotnet.microsoft.com/download)
* [Docker latest version](https://docs.docker.com/engine/install/ubuntu/)
* [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [aws ecs cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)

## Requirements Installation on Ubuntu 

* [.NET Core 3.0](https://dotnet.microsoft.com/download)
  ```bash
  # Add the Microsoft package signing key to tour list of trusted keys and add the package repository
  wget https://packages.microsoft.com/config/ubuntu/20.10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  # Install the SDK
  sudo apt-get update; \
  sudo apt-get install -y apt-transport-https && \
  sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-5.0
  ```
* [Docker latest version](https://docs.docker.com/engine/install/ubuntu/)
```bash
# Uninstall old versions of docker
sudo apt-get remove docker docker-engine docker.io containerd runc
# Setup the Repository
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Set up the stable repository
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose
# Allow Docker to run without sudo
sudo groupadd docker
sudo gpasswd -a $USER docker
```
* [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
```bash
sudo apt install unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
* [aws ecs cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)
```bash
sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli
### Verify the CLI is wroking properly
ecs-cli --version
```

# Creating the Application

To begin, follow the aws sample steps for an AWS ECS Fargate .NET Core application. The repository for this sample app are maintained [here](). Follow the instructions there for a complete explanation -- or follow the below condensed version to get started quickly.

## Run the Application locally

Clone the repository, set as active directory
```
git clone https://github.com/aws-samples/amazon-ecs-fargate-aspnetcore.git
cd amazon-ecs-fargate-aspnetcore/mymvcweb
```
Create ASP.NET core mvc application
```bash
mkdir mymvcweb
cd mymvcweb
dotnet new mvc
dotnet restore
dotnet build
dotnet publish -c "Release"
```

Build and run these containers on local
```bash
#Rename Dockerfile to supported filename
mv Docker-compose.yml docker-compose.yml
#Build and run
sudo docker-compose build
sudo docker-compose up
```

Verify the application is running locally by confirming a non-error response from
```bash
curl localhost:80
```
## Push to ECS

Edit the file `reverseproxy/nginx.conf` and change the value of `server mymvcweb:5000` to `server 127.0.0.1:5000`. Equivalently, run the below command in the `reverseproxy` directory.
```bash
sed -i 's/mymvcweb:5000/127.0.0.1:5000/g' nginx.conf
```

If not done already, AWS CLI credentials will need to be configured by running `aws configure` before proceeding. _Note the remaining commands are hard-coded for the region `us-west-2`, adjust as needed_. For ease of use, set the your AWS account number as an environmental variable.
```bash
export AWS_ACCOUNT_NUMBER=
```

Next, follow the AWS instructions published here, starting at the heading *Push container images to ECR*, or for a faster-less explained path, follow below.
```bash
# Log into AWS ECR and Docker
aws ecr get-login-password --region us-west-2 | sudo docker login --username AWS --password-stdin $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com
# Tag the local container image (for mymvcweb) with the remote ECR repository
sudo docker tag amazon-ecs-fargate-aspnetcore_mymvcweb:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest 
# Push the 'mymvcweb' image to the remote 'mymvcweb' repository
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest 
# Tag the local container image (for reverseproxy) with the remote ECR repository
sudo docker tag amazon-ecs-fargate-aspnetcore_reverseproxy:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
# Push the 'reverseproxy' image to the remote 'mymvcweb' repository
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
```

For this section, follow the screenshots for [Create ECS Fargate Cluster](https://github.com/aws-samples/amazon-ecs-fargate-aspnetcore#create-ecs-fargate-cluster).
# Add Monitoring

Once the application has been verified to be properly running it is time to add in some monitoring.

### Smart Agent

By installing the Smart Agent, metrics can be shipped to the Infrastructure Monitor. Follow the recommended Smart Agent [deployment instructions for fargate](https://github.com/signalfx/signalfx-agent/tree/master/deployments/fargate).

### Viewing metrics in the Infrastructure Monitor

Since the Smart Agent wasn't technically installed on a _host_, the metrics will all be collected for the _containers_. Navigate to Infrastructure >> Docker Containers.

## APM

### Instrumentation

### Viewing traces in the APM

Let's further verify that the instrumentation and agent installation were successful by creating some requets on the application and ensuring that they are viewable in the APM.
