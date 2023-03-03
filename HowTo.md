# Setup Details

## Building Chromium on Ubuntu 

To make sure of available space for chromium setup
Change HOME dir to /proj/FEC, path which has sufficient space

apt install gperf

apt install libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev

Follow 
https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md

chrome --version

## Building QUIC 

gn gen out/Debug

https://www.chromium.org/quic/playing-with-quic/


## Get chrome driver 

https://chromedriver.chromium.org/downloads/version-selection