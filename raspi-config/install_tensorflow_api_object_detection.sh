cd ~/home/pi/Vision-Car/models/research
echo "Installing tensorflow api object_detection..."
python use_protobuf.py
python object_detection/protos protoc
python -m pip3 install .
echo "Terminé."