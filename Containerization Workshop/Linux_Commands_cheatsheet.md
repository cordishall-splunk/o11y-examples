| Command | Usage | Example | Purpose |
|---|---|---|---|
| ls | ls | ls | List the items in the active directory |
| cd | cd <directory> | cd /etc/otel/collector | Navigate to the specified directory |
| cd .. | cd .. | cd .. | Navigate up one directory level |
| pwd | pwd | pwd | List the current active directory |
| clear | clear | clear | Clear the terminal screen |
| history | history | history | List the previously ran commands |
| nano | nano <file> | nano agent_config.yaml | Edit a file |
| sudo | sudo <command> | sudo nano agent_config.yaml | Execute subsequent command as the root user |
| chmod | chmod ### <file> | chmod 400 ec2_access.pem | Change the permissions of a file |
| git clone | git clone <url> | git clone https://github.com/cordishall-splunk/o11y-examples.git | Clone a directory locally |
| export | export key=value | export ACCESS_TOKEN=1234abcdef | Set an environmental variable |
| docker build | docker build <path to dockerfile> | docker build --tag server-py . | Build a container container image using given dockerfile |
| docker images | docker images | docker images | List the available container images |
| docker run | docker run <container_image> | docker run --publish 5000:5000 server-py | Run a docker image |
| [Cntrl + c] | [Cntrl + c] | [Cntrl + c] | Abort whatever process is running in the terminal. Stopping a container, or python service for example |
| [Cntrl + d] | [Cntrl + d] | [Cntrl + d] | Exit the current shell session. For example, terminate an ssh session on a remote host |
| [Tab] | [Tab] | [Tab] | Autocomplete whatever you're typing |
| journalctl -u splunk-otel-collector.service -f | journalctl -u splunk-otel-collector.service -f | journalctl -u splunk-otel-collector.service -f | Tail the logs of the spllunk otel collector |
| systemctl restart splunk-otel-collector | systemctl restart splunk-otel-collector | systemctl restart splunk-otel-collector | Restart the splunk otel collector service. Command must be run in order to update config after editing /etc/otel/collector/agent_config.yaml |