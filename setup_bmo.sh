sudo sed -i -e 's/$/ video=HDMI-A-1:480x800M,rotate=90/' /boot/firmware/cmdline.txt
sudo apt -y install git python3-pip libgl1-mesa-glx libgles2-mesa libegl1-mesa libmtdev1 libavcodec-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libavfilter-dev libavdevice-dev
echo "# Common aliases/shortcuts" >> .bash_profile
echo "#" >> .bash_profile
echo "alias ls='ls --color=auto'" >> .bash_profile
echo "alias act='source ./venv/bin/activate'" >> .bash_profile
echo "alias deact='deactivate'" >> .bash_profile
echo "alias ll='ls -alF'" >> .bash_profile
echo "alias renv='deactivate; rm -rf ./venv; python -m venv ./venv; source ./venv/bin/activate; pip install -r requirements.txt'" >> .bash_profile

mkdir ~/work
mkdir ~/work/bmo



