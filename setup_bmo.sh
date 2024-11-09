# sudo sed -i -e 's/$/ video=HDMI-A-1:480x800M,rotate=90/' /boot/firmware/cmdline.txt
sudo apt -y install git python3-pip libgl1-mesa-glx libgles2-mesa libegl1-mesa libmtdev1 libavcodec-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libavfilter-dev libavdevice-dev
echo "# Common aliases/shortcuts" >> .bash_profile
echo "#" >> .bash_profile
echo "alias ls='ls --color=auto'" >> .bash_profile
echo "alias act='source ./venv/bin/activate'" >> .bash_profile
echo "alias deact='deactivate'" >> .bash_profile
echo "alias ll='ls -alF'" >> .bash_profile
echo "alias renv='deactivate; rm -rf ./venv; python -m venv ./venv; source ./venv/bin/activate; pip install -r requirements.txt'" >> .bash_profile

# Setup 5" Elecrow RC050 display
sudo echo "# HDMI stuff" >> /boot/firmware/config.txt
sudo echo "hdmi_force_hotplug=1" >> /boot/firmware/config.txt
sudo echo "max_usb_current=1" >> /boot/firmware/config.txt
sudo echo "hdmi_drive=1" >> /boot/firmware/config.txt
sudo echo "hdmi_group=2" >> /boot/firmware/config.txt
sudo echo "hdmi_mode=1" >> /boot/firmware/config.txt
sudo echo "hdmi_cvt=800 480 60 6 0 0 0" >> /boot/firmware/config.txt
sudo echo "display_rotate=0" >> /boot/firmware/config.txt

mkdir -p ~/work
mkdir -p ~/work/bmo

# Setup github
echo "Please enter your github account name (email):"
read gh_email
ssh-keygen -t ed25519 -C "$gh_email"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
echo "Copy the contents of this file to your github ssh setup"
cat ~/.ssh/id_ed25519.pub
read -p "Press Enter to continue..."

# Git BMO
cd ~/work
git clone https://github.com/jpeters71/bmo.git

# https://www.waveshare.com/wiki/WM8960_Audio_HAT
cd ~/work
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh
sudo reboot
