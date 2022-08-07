# Install the Krach-Generator as a Systemd service

This directory contains a sample service file.
It asumes that the reposirory was cloned into /opt/krach-generator.
If this is not the case, change the paths accordingly.

## Steps to install as a service:

- Clone into /opt/krach-generator (Optional, see above)
- Run make venv in /opt/krach-generator
- Copy the service file to /etc/systemd/system
- run systemctl daemon-reload
- run systemctl enable krgen.service
- run systemctl start krgen.service

