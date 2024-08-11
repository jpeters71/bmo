sudo echo 'video=HDMI-A-1:480x800M,rotate=90' >> /boot/firmware/cmdline.txt

sudo apt install git python3-pip libgl1-mesa-glx libgles2-mesa libegl1-mesa libmtdev1
python -m pip install "kivy[base]" kivy_examples ffpyplayer

git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./MHS35-show