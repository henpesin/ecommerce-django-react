# Vagrantfile for setting up Jenkins and Application servers

Vagrant.configure("2") do |config|
  # Define Jenkins server
  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "ubuntu/bionic64"
    jenkins.vm.network "private_network", ip: "192.168.56.10"
    jenkins.vm.hostname = "jenkins"
    
    # Port forwarding for Jenkins
    jenkins.vm.network "forwarded_port", guest: 8080, host: 8080
    
    jenkins.vm.provider "virtualbox" do |vb|
      vb.name = "jenkins-server"
      vb.memory = "2048"
      vb.cpus = 2
    end

    jenkins.vm.provision "shell", inline: <<-SHELL
      # Update package list and upgrade all packages
      sudo apt-get update
      sudo apt-get upgrade -y

      # Temporarily download and install init-system-helpers from Debian repository
      wget http://ftp.us.debian.org/debian/pool/main/i/init-system-helpers/init-system-helpers_1.60_all.deb
      sudo dpkg -i init-system-helpers_1.60_all.deb
      sudo apt-get -f install -y
      rm init-system-helpers_1.60_all.deb

      # Install required dependencies for Jenkins
      sudo apt-get install -y software-properties-common apt-transport-https ca-certificates fontconfig

      # Install Java 17
      sudo apt-get install -y wget
      wget -O- https://apt.corretto.aws/corretto.key | sudo apt-key add -
      sudo add-apt-repository 'deb https://apt.corretto.aws stable main'
      sudo apt-get update
      sudo apt-get install -y java-17-amazon-corretto-jdk

      # Add Jenkins repository and GPG key
      wget -q -O - https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo apt-key add -
      sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
      sudo apt-get update

      # Install Jenkins
      sudo apt-get install -y jenkins

      # Set java.awt.headless=true
      sudo sed -i 's/JENKINS_ARGS="\(.*\)"/JENKINS_ARGS="\1 -Djava.awt.headless=true"/' /etc/default/jenkins
      
      # Start Jenkins
      sudo systemctl start jenkins
      sudo systemctl enable jenkins

      # Configure sudoers file for Jenkins user
      echo "jenkins ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/jenkins
    SHELL
  end

  # Define Application server
  config.vm.define "app" do |app|
    app.vm.box = "ubuntu/bionic64"
    app.vm.network "private_network", ip: "192.168.56.11"
    app.vm.hostname = "app"
    
    # Port forwarding for the application
    app.vm.network "forwarded_port", guest: 8000, host: 8000  # Adjust the guest port as needed
    
    app.vm.provider "virtualbox" do |vb|
      vb.name = "app-server"
      vb.memory = "2048"
      vb.cpus = 2
    end

    app.vm.provision "shell", inline: <<-SHELL
      # Update package list
      sudo apt-get update
      
      # Install Docker
      sudo apt-get install -y docker.io
      sudo usermod -aG docker vagrant
      
      # Install Docker Compose
      sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose

      # Install dependencies for the app (e.g., Python, Node.js)
      sudo apt-get install -y python3.9 python3.9-venv python3-pip
      sudo apt-get install -y nodejs npm
    SHELL
  end
end
