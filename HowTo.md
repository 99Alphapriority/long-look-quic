# Setup Details

## Building Chromium on Ubuntu 

To make sure of available space for chromium setup
Change HOME dir to /proj/FEC, path which has sufficient space

```bash
sudo apt install gperf
sudo apt install libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev
```

Follow 
https://chromium.googlesource.com/chromium/src/+/main/docs/linux/build_instructions.md

chrome --version

## Get chrome driver 

https://chromedriver.chromium.org/getting-started
https://chromedriver.chromium.org/downloads/version-selection

## Building QUIC 

```bash
gn gen out/Debug
```

Follow
https://www.chromium.org/quic/playing-with-quic/

```bash
# quic server
out/Debug/quic_server --quic_response_cache_dir=/proj/FEC-HTTP/long-quic/quic-data/www.example.org   --certificate_file=net/tools/quic/certs/out/leaf_cert.pem --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8

# quic client
out/Debug/quic_client --host=10.10.1.1 --port=6121 --allow_unknown_root_cert https://www.example.org/

```

Use Chromium as client

Due to issue in running chromium --headless in VM with not display. Only selenium script is used.


## Building HTTPS server ( HTTP/2 , TLS, TCP )

Apache2   
[Get Apache2](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-22-04)

Flask




# Sources:

1. TownesZhou [CS536-Network-Project](https://github.com/TownesZhou/CS536-Network-Project)