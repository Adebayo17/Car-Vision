cd
echo "Installing libcamera..."
git clone https://git.libcamera.org/libcamera/libcamera.git
cd libcamera
meson setup build
ninja -C build install
echo "Terminé: installation libcamera"

echo "Testing..."
libcamera-hello
echo "Terminé: testing"