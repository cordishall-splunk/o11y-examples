cd mymvcweb
rm Dockerfile
wget https://raw.githubusercontent.com/cordishall-splunk/o11y-examples/ecs-fargate-netcore/ecs-fargate-aspentcore/Samples/mymvcwebSamples/Dockerfile
cd ../reverseproxy
rm Dockerfile
wget https://raw.githubusercontent.com/cordishall-splunk/o11y-examples/ecs-fargate-netcore/ecs-fargate-aspentcore/Samples/reverseproxySamples/Dockerfile
sudo docker-compose build
sudo docker tag amazon-ecs-fargate-aspnetcore_mymvcweb:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest 
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/mymvcweb:latest 
sudo docker tag amazon-ecs-fargate-aspnetcore_reverseproxy:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest
sudo docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-west-2.amazonaws.com/reverseproxy:latest