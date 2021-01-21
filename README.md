# Installation on ubuntu

1. Set up docker repository
   ```
   sudo apt-get update
   sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```
2. Install docker engine
   ```
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   sudo docker run hello-world
   ```
3. Manage Docker as a non-root user
   ```
   sudo usermod -aG docker $USER
   ```
4. Log out and log back in so that your group membership is re-evaluated
   ```
   docker run hello-world
   ```
5. Remap docker root user to local user
   ```
   echo "$(id -un):$(id -u):65536" | sudo tee /etc/subuid
   echo "$(id -gn):$(id -g):65536" | sudo tee /etc/subgid
   echo "{\"userns-remap\":\"$(id -un)\"}" | sudo tee /etc/docker/daemon.json
   sudo systemctl restart docker
   sudo ls -la /var/lib/docker
   ```
6. Install docker-compose
   ```
   sudo curl -L "https://github.com/docker/compose/releases/download/1.28.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
7. Generate rsa key pair with **no** passphrase
8. Add your public rsa key to <https://gitlab.tvbit.co:4115/profile/keys>
9. Clone the repository
   ```
   git clone https://github.com/lordofbuckwheat/devenv
   cd devenv
   mkdir config
   ```
10. Copy your `.gitconfig` and private rsa key to `config` directory. `.gitconfig` example:
   ```
   [user]
       name = lordofbuckwheat
       email = lord.of.buckwheat@gmail.com
   ```
11. ```
    docker-compose build
    docker-compose up -d
    docker-compose logs -f
    ```
12. After containers are up connect to `ws` with
   ```
   ./connect.sh
   ```
13. Add rootCA.pem to your trusted certificate authorities