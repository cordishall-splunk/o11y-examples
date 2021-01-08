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

Create a new folder

```bash
mkdir amazon-ecs-fargate-aspnetcore; cd amazon-ecs-fargate-aspnetcore
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
Create a new file named `Dockerfile` with the below contents
```
FROM mcr.microsoft.com/dotnet/core/sdk:3.0 AS build-env

WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out



# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "mymvcweb.dll"]

ENV ASPNETCORE_URLS http://+:5000
EXPOSE 5000
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

By installing the Smart Agent, metrics can be shipped to the Infrastructure Monitor. The full example of a recommended Smart Agent [deployment in fargate is here](https://github.com/signalfx/signalfx-agent/tree/master/deployments/fargate).

To add the agent to an existing cluster, find the task definition which you would like to add monitoring and create a new revision. At the bottom of the page select 'Configure via JSON' and find the list of `containerDefinition` and add the following element, filling in the applicable values for `MY_ACCESS_TOKEN`, `SFX_INGEST_URL`, `SFX_API_URL`. To be safe, use a tool like [jsonlint](https://jsonlint.com) to verify the syntax.
```json
{
  "entryPoint": [
      "bash",
      "-c"
  ],
  "portMappings": [],
  "command": [
      "curl --fail $CONFIG_URL > /etc/signalfx/agent.yaml && exec /bin/signalfx-agent"
  ],
  "environment": [
      {
          "name": "ACCESS_TOKEN",
          "value": "MY_ACCESS_TOKEN"
      },
      {
          "name": "INGEST_URL",
          "value": "SFX_INGEST_URL"
      },
      {
          "name": "API_URL",
          "value": "SFX_API_URL"
      },
      {
          "name": "CONFIG_URL",
          "value": "https://raw.githubusercontent.com/signalfx/signalfx-agent/v5.7.1/deployments/fargate/agent.yaml"
      }
  ],
  "dockerLabels": {
      "app": "signalfx-agent"
  },
  "name": "signalfx-agent",
  "image": "quay.io/signalfx/signalfx-agent:5.7.1"
}
```
If you are unsure about the config values to use...
* `ACCESS_TOKEN` -- In Splunk Infrastructure Monitor navigate to _Settings_ in the top right (your user profile), then _Organization Settings_ >> _Access Tokens_.
* `SFX_INGEST_URL` -- `https://ingest.YOUR_SIGNALFX_REALM.signalfx.com`
* `SFX_API_URL` -- `https://api.YOUR_SIGNALFX_REALM.signalfx.com`
* `YOUR_SIGNALFX_REALM` -- for the above two points, note the realm that your organization is in. The easiest way to find out is by looking at the url; for example, `https://app.us1.signalfx.com` would be `us1.`

Save the updated Task Definition, then in the already running cluster update the service to the latest revision.

### Viewing metrics in the Infrastructure Monitor

Since the Smart Agent wasn't technically installed on a _host_, the metrics will all be collected for the _containers_. Navigate to Infrastructure >> Docker Containers. The containers from the cluster will show up here momentarily. Additionally, there will be an out of the box ECS dashboard found at _Dashboards_ >> _ECS_ >> _ECS (SignalFx) Cluster_ (among some others in the group).

## APM

### Instrumentation

For instrumenting a .NET Core application the below steps are based off of the complete documentation found [here](https://github.com/signalfx/signalfx-dotnet-tracing). For this example, the only thing that needs to be added is a block to the Dockerfile which will add the SignalFx auto-instrumentation to the image. Add the below snippet to the Dockerfile for both mymvcweb and reverseproxy.
```
# Custom lines Adding the SignalFx Auto-Instrumentation to the image:

# First install the package. This example downloads the latest version
# alternatively download a specific version or use a local copy.
ARG TRACER_VERSION=0.1.3
ADD https://github.com/signalfx/signalfx-dotnet-tracing/releases/download/v${TRACER_VERSION}/signalfx-dotnet-tracing_${TRACER_VERSION}_amd64.deb /signalfx-package/signalfx-dotnet-tracing.deb
RUN dpkg -i /signalfx-package/signalfx-dotnet-tracing.deb
RUN rm -rf /signalfx-package

# Prepare the log directory (useful for local tests).
RUN mkdir -p /var/log/signalfx/dotnet && \
    chmod a+rwx /var/log/signalfx/dotnet

# Set the required environment variables. In the case of Azure Functions more
# can be set either here or on the application settings. 
ENV CORECLR_ENABLE_PROFILING=1 \
    CORECLR_PROFILER='{B4C89B0F-9908-4F73-9F59-0D77C5A06874}' \
    CORECLR_PROFILER_PATH=/opt/signalfx-dotnet-tracing/SignalFx.Tracing.ClrProfiler.Native.so \
    SIGNALFX_INTEGRATIONS=/opt/signalfx-dotnet-tracing/integrations.json \
    SIGNALFX_DOTNET_TRACER_HOME=/opt/signalfx-dotnet-tracing
# End of SignalFx customization.
```

After the changes, rebuild the container images and push them to ECR.
```bash
sudo docker-compose build
sudo docker tag amazon-ecs-fargate-aspnetcore_mymvcweb:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest
sudo docker tag amazon-ecs-fargate-aspnetcore_reverseproxy:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
```

Last, the AWS resources need to be updated. First, update the Task Definition by selecting aspnetcorefargatetask and then _Create New Revision_, for both mymvcweb and reverseproxy click into the container and click _Update_. Second, navigate to the cluster and select the Services >> aspnetcorefargatesvc and click _Update_. Under the task definition, update to the latest revision of the task definition.


### Viewing traces in the APM

Let's further verify that the instrumentation and agent installation were successful by creating some requets on the application and ensuring that they are viewable in the APM.

# Troubleshooting

### Containers are cycling up and down and I can't load the app in the browser

Check the logs of the container, if within the logs you see something like
```
nginx: [emerg] host not found in upstream "mymvcweb:5000" in /etc/nginx/nginx.conf:10
```
The step to replace `mymvcweb` with `127.0.0.1` may have been missed. Verify that before building and pushing the container images that the file `reverseproxy/nginx.conf` has the aforementioned substitution made. If not, make the change, rebuild and repush container images and then update the service definition to use the new revision. Running the below from the `reverseproxy` directory will quickly do that...
```bash
sed -i 's/mymvcweb:5000/127.0.0.1:5000/g' nginx.conf
cd ..
sudo docker-compose build
sudo docker tag amazon-ecs-fargate-aspnetcore_reverseproxy:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
```
Last, update the task definition to use the new version of reverseproxy.

### Traces aren't showing up
