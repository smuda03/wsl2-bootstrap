#!/bin/bash

echo ""
echo "##########################################################################################################################################"
echo "# Install Packages"
echo "##########################################################################################################################################"
echo ""

sudo apt update

# Install Packages
sudo apt install -y curl git iproute2 lsb-release openssh-server python3-virtualenv socat sshfs tmux unzip wget zip zsh zsh-autosuggestions zsh-syntax-highlighting

echo ""
echo "##########################################################################################################################################"
echo "Packages installed"
echo "##########################################################################################################################################"
echo ""

##########################################################################################################################################
# Install and configure wsl2-ssh-pageant
##########################################################################################################################################
if [ ! -f "$HOME/bin/wsl2-ssh-pageant.exe" ]; then
    mkdir -p "$HOME/bin"
    wget -O "$HOME/bin/wsl2-ssh-pageant.exe" "https://github.com/BlackReloaded/wsl2-ssh-pageant/releases/latest/download/wsl2-ssh-pageant.exe"
    # Set the executable bit.
    chmod +x "$HOME/bin/wsl2-ssh-pageant.exe"
else
    echo ""
    echo "wsl2-ssh-pageant.exe already installed"
    echo ""
fi

mkdir -p $HOME/.ssh
chmod 700 $HOME/.ssh

if [ ! -f "$HOME/.bash_pagent" ]; then
    cat << 'EOF' >> $HOME/.bash_pagent
export SSH_AUTH_SOCK="$HOME/.ssh/agent.$(lsb_release -cs).sock"
if ! ss -a | grep -q "$SSH_AUTH_SOCK"; then
  rm -f "$SSH_AUTH_SOCK"
  wsl2_ssh_pageant_bin="$HOME/bin/wsl2-ssh-pageant.exe"
  if test -x "$wsl2_ssh_pageant_bin"; then
    (setsid nohup socat UNIX-LISTEN:"$SSH_AUTH_SOCK,fork" EXEC:"$wsl2_ssh_pageant_bin" >/dev/null 2>&1 &)
  else
    echo >&2 "WARNING: $wsl2_ssh_pageant_bin is not executable."
  fi
  unset wsl2_ssh_pageant_bin
fi
EOF
    echo ""
    echo "$HOME/.bash_pagent created"
    echo ""
else
    echo ""
    echo "$HOME/.bash_pagent already exists"
    echo ""
fi


if ! grep -qF 'if [ -f ~/.bash_pagent ]; then' "$HOME/.bashrc"; then
    cat << 'EOF' >> "$HOME/.bashrc"

if [ -f ~/.bash_pagent ]; then
    . ~/.bash_pagent
fi
EOF
    echo ""
    echo "$HOME/.bash_pagent added to .bashrc"
    echo ""
else
    echo ""
    echo "$HOME/.bash_pagent already exists in .bashrc"
    echo ""
fi

echo ""
echo "##########################################################################################################################################"
echo "wsl2-ssh-pageant installed and configured"
echo "##########################################################################################################################################"


echo ""
echo ""
echo "##########################################################################################################################################"
echo "# Configure Git"
echo "# Enter your name and email address to configure git"
echo "##########################################################################################################################################"
echo ""
# Set the username and email address
# Ask for name and email interactively
read -p "Enter your name: " name
read -p "Enter your email: " email

# Set the username and email address
git config --global user.name "$name"
git config --global user.email "$email"
# Set the credential helper
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
# Set the default branch name
git config --global init.defaultBranch main

echo ""
echo ""
echo "##########################################################################################################################################"
echo "# HashiCorp Tools"
echo "##########################################################################################################################################"
echo ""

if [ -f /usr/share/keyrings/hashicorp-archive-keyring.gpg ] && [ -f /etc/apt/sources.list.d/hashicorp.list ]; then
    echo "HashiCorp GPG key and repository was already added."
    echo ""
else 
    echo ""
    read -p "Do you want add the HashiCorp APT Repository? (y/n): " install_hashicorp
    echo ""

    if [ "$install_hashicorp" = "y" ]; then
        if [ ! -f "/usr/share/keyrings/hashicorp-archive-keyring.gpg" ]; then
            wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        fi

        if [ ! -f "/etc/apt/sources.list.d/hashicorp.list" ]; then
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
            sudo apt update
        fi
    fi
fi