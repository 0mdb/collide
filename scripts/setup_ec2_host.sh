#!/bin/bash

# Exit immediately on errors
set -e

# Update system and install Docker
function install_docker() {
  sudo yum -y update && sudo yum -y install docker
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo usermod -aG docker "$USER"
}

# Install Git
function install_git() {
    sudo yum -y install git
}

# Set up Traefik
function setup_traefik() {
  local base_domain="$1"
  local base_name="$2"
  local env_name_short="$3"
  local env_name_long="$4"
  local traefik_username="$5"
  local traefik_password="$6"
  local traefik_email="$7"

  # Set hostname
  local use_hostname="$env_name_short.$base_domain"
  sudo printf '%s\n' "$use_hostname" > /etc/hostname
  sudo hostname -F /etc/hostname

  # Initialize Docker Swarm
  docker swarm init
  docker node ls

  # Create Traefik network
  docker network create --driver=overlay traefik-public
  local node_id=$(docker info -f '{{.Swarm.NodeID}}')
  docker node update --label-add traefik-public.traefik-public-certificates=true "$node_id"

  # Deploy Traefik stack
  local email="$traefik_email"
  local domain="traefik.$env_name_short.$base_domain"
  local username="$traefik_username"
  local password="$traefik_password"
  local hashed_password=$(openssl passwd -apr1 "$password")
  curl -L dockerswarm.rocks/traefik.yml -o traefik.yml
  docker stack deploy -c traefik.yml traefik
  docker stack ps traefik
}

# Install Docker and set up Traefik
function install_and_setup() {
  install_docker
  setup_traefik "$BASE_DOMAIN" "$BASE_NAME" "$ENV_NAME_SHORT" "$ENV_NAME_LONG" "$TRAEFIK_USERNAME" "$TRAEFIK_PASSWORD" "$TRAEFIK_EMAIL"
}

# Install Docker Compose
function install_docker_compose() {
  curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
  source ~/.bashrc
  docker-compose --version
}

# Install required Python library
function install_python_library() {
  sudo yum -y install python3-pip
  pip3 install docker-auto-labels
  pip3 install PyYAML==4.2b4
}

# Set configuration variables
BASE_DOMAIN=lobbyradar.io
BASE_NAME=lobbyradar-io
ENV_NAME_SHORT=stag
ENV_NAME_LONG=staging
TRAEFIK_USERNAME=admin
TRAEFIK_PASSWORD=changethis
TRAEFIK_EMAIL=info@$BASE_DOMAIN

# Install Docker and set up Traefik
install_and_setup

# Install Docker Compose
install_docker_compose

# Install required Python library
install_python_library

# Install Git
install_git

# Reboot system
read -p "Reboot system now? (y/n) " choice
case "$choice" in
  y|Y ) reboot;;
  n|N ) exit 0;;
  * ) echo "Invalid choice, assuming 'no'"; exit 0;;
esac
