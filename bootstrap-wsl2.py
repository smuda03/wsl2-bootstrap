import subprocess

print("")
print("##########################################################################################################################################")
print("# Install Packages")
print("##########################################################################################################################################")
print("")

subprocess.run(["sudo", "apt", "update"])

# Install Packages
subprocess.run(["sudo", "apt", "install", "-y", "curl", "git", "iproute2", "lsb-release", "openssh-server", "python3-virtualenv", "socat", "sshfs", "tmux", "unzip", "wget", "zip", "zsh", "zsh-autosuggestions", "zsh-syntax-highlighting"])

print("")
print("##########################################################################################################################################")
print("Packages installed")
print("##########################################################################################################################################")
print("")

##########################################################################################################################################
# Install and configure wsl2-ssh-pageant
##########################################################################################################################################
if not os.path.exists(os.path.expanduser("~/bin/wsl2-ssh-pageant.exe")):
    os.makedirs(os.path.expanduser("~/bin"))
    subprocess.run(["wget", "-O", os.path.expanduser("~/bin/wsl2-ssh-pageant.exe"), "https://github.com/BlackReloaded/wsl2-ssh-pageant/releases/latest/download/wsl2-ssh-pageant.exe"])
    # Set the executable bit.
    subprocess.run(["chmod", "+x", os.path.expanduser("~/bin/wsl2-ssh-pageant.exe")])
else:
    print("")
    print("wsl2-ssh-pageant.exe already installed")
    print("")

os.makedirs(os.path.expanduser("~/.ssh"), exist_ok=True)
subprocess.run(["chmod", "700", os.path.expanduser("~/.ssh")])

if not os.path.exists(os.path.expanduser("~/.bash_pagent")):
    with open(os.path.expanduser("~/.bash_pagent"), "w") as f:
        f.write('''export SSH_AUTH_SOCK="$HOME/.ssh/agent.$(lsb_release -cs).sock"
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
''')
    print("")
    print("~/.bash_pagent created")
    print("")
else:
    print("")
    print("~/.bash_pagent already exists")
    print("")

bashrc_path = os.path.expanduser("~/.bashrc")
if not any("if [ -f ~/.bash_pagent ]; then" in line for line in open(bashrc_path)):
    with open(bashrc_path, "a") as f:
        f.write('''
if [ -f ~/.bash_pagent ]; then
    . ~/.bash_pagent
fi
''')
    print("")
    print("~/.bash_pagent added to .bashrc")
    print("")
else:
    print("")
    print("~/.bash_pagent already exists in .bashrc")
    print("")

print("")
print("##########################################################################################################################################")
print("wsl2-ssh-pageant installed and configured")
print("##########################################################################################################################################")

print("")
print("")
print("##########################################################################################################################################")
print("# Configure Git")
print("# Enter your name and email address to configure git")
print("##########################################################################################################################################")
print("")
# Set the username and email address
# Ask for name and email interactively
name = input("Enter your name: ")
email = input("Enter your email: ")

# Set the username and email address
subprocess.run(["git", "config", "--global", "user.name", name])
subprocess.run(["git", "config", "--global", "user.email", email])
# Set the credential helper
subprocess.run(["git", "config", "--global", "credential.helper", "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"])
# Set the default branch name
subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])

print("")
print("")
print("##########################################################################################################################################")
print("# HashiCorp Tools")
print("##########################################################################################################################################")
print("")

hashicorp_keyring_path = "/usr/share/keyrings/hashicorp-archive-keyring.gpg"
hashicorp_list_path = "/etc/apt/sources.list.d/hashicorp.list"

if os.path.exists(hashicorp_keyring_path) and os.path.exists(hashicorp_list_path):
    print("HashiCorp GPG key and repository was already added.")
    print("")
else:
    print("")
    install_hashicorp = input("Do you want add the HashiCorp APT Repository? (y/n): ")
    print("")

    if install_hashicorp == "y":
        if not os.path.exists(hashicorp_keyring_path):
            subprocess.run(["wget", "-O-", "https://apt.releases.hashicorp.com/gpg", "|", "sudo", "gpg", "--dearmor", "-o", hashicorp_keyring_path])

        if not os.path.exists(hashicorp_list_path):
            subprocess.run(["echo", f'deb [arch=$(dpkg --print-architecture) signed-by={hashicorp_keyring_path}] https://apt.releases.hashicorp.com $(lsb_release -cs) main', "|", "sudo", "tee", hashicorp_list_path])
            subprocess.run(["sudo", "apt", "update"])

