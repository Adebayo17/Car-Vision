import wget
model_link = "https://github.com/protocolbuffers/protobuf/releases/download/v23.1/protoc-23.1-linux-x86_64.zip"
wget.download(model_link)
import tarfile
tar = tarfile.open('protoc-23.1-linux-x86_64.zip')
tar.extractall('.')
tar.close()