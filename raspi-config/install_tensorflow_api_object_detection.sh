cd ~
python protoc_downloader.py
export PATH=$PATH:/home/pi/protoc-23.1-linux-x86_64/bin
echo $PATH
echo "Add path in bashrc at the end of file"
nano ~/.bashrc
source ~/.bashrc
echo "Installing tensorflow api object_detection..."
pip install object-detection-0.1==0.1
echo "Terminé."