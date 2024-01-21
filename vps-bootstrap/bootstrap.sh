#!/bin/sh

#
# debian 12
#
#   installs docker
#   installs ftp server

apt update
apt upgrade -y

apt install ca-certificates curl gnupg -Y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg


echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
   tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update

apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin vsftpd  -y

# Define the properties
properties=("anonymous_enable=NO" "local_enable=YES" "write_enable=YES")

# Loop through the properties
for property in "${properties[@]}"; do
    # Extract the key and value
    key=$(echo $property | cut -d'=' -f1)
    value=$(echo $property | cut -d'=' -f2)

    # Check if the key exists in the file
    if grep -q "^$key" /etc/vsftpd.conf; then
        # If the key exists, update its value
        sed -i "s/^$key=.*/$key=$value/" /etc/vsftpd.conf
    else
        # If the key does not exist, append it to the file
        echo "$key=$value" >> /etc/vsftpd.conf
    fi
done