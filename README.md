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
11. Add hosts to your /etc/hosts:
    ```
    127.0.0.1 public.tvbit.local
    127.0.0.1 admin.tvbit.local
    127.0.0.1 go.tvbit.local
    127.0.0.1 master.tvbit.local
    ```
12. Add rootCA.pem to your trusted certificate authorities. In Chrome go to Settings -> Security -> Manage certificates -> Authorities -> Import
13. ```
    docker-compose build
    docker-compose up -d
    docker-compose logs -f
    ```
14. After containers are up connect to `ws` with
    ```
    ./connect.sh
    ```
15. Run commands in `ws` container:
    - start client server:
      ```
      cd ~/scripts
      ./run.sh
      ```
    - run angular in production mode
      ```
      cd ~/app/supertvbit/public/panel
      npm run prod
      ```
    - run angular in development mode
      ```
      cd ~/app/supertvbit/public/panel
      npm run start
      ```
16. Services available on docker host:
    - admin panel in production mode:
      ```
      http://public.tvbit.local:10080/admin
      https://public.tvbit.local:10443/admin
      ```
    - admin panel in development mode:
      ```
      http://localhost:14200/admin
      http://admin.tvbit.local:10080/admin
      ```
    - client server api:
      ```
      http://go.tvbit.local:18285
      https://go.tvbit.local:18286
      ```
    - master server:
      ```
      https://master.tvbit.local:10443
      ```