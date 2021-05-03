# WIP RUM example

# Hello World

Create the simplest working example of Splunk RUM! Start by starting a new EC2 instance, ensure that both port 80 is open for inbound traffic in the security group.

In the EC2 instance command line, type
```
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
curl https://gist.githubusercontent.com/chrisvfritz/bc010e6ed25b802da7eb/raw/18eaa48addae7e3021f6bcea03b7a6557e3f0132/index.html > /var/www/html/index.html
```

You should now be able to navigate to your new web server at http://<ec2-public-ipv4>.com.

Add RUM instrumentation in Splunk Obsevability. Start by creating a new RUM Access Token (selecting the checkbox for _only_ RUM) under Organization Settings > Access Tokens > New Token -- admin required. Under Data Setup > RUM Instrumentation, follow the instruction setup wizard, paste the script under the <head> tag in /var/www/html/index.html.

In your browser refresh your EC2 webserver, with developer tools, verify that the RUM script is in place. You should see traffic reflected in Splunk RUM in real time.
