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


## Starting Servers


### TCP

```bash
# simple python server
python server.py  

# OR

# Apache + Flask
# TODO
```

### QUIC

```bash
# start quic server
quic_server
```



## Automating Test

Selenium to driver browser and Python scripts for everything else.


## Getting Metrics

* Selenium
* chrome-har-capturer - Gets details network stats

### HAR capturer

**Install**
npm install -g chrome-har-capturer


**Start chromium headless for quic**
```bash
out/Default/chrome  --no-sandbox --headless --disable-gpu --remote-debugging-port=9222  --user-data-dir=/tmp/chrome-profile  --ignore-certificate-errors-spki-list=Tz6CyL8WC55nA6yDXagMahDsUFOBBA+slB7q3RphY88=  --no-proxy-server   --enable-quic   --origin-to-force-quic-on=www.examplequic.org:443   --host-resolver-rules='MAP www.examplequic.org:443 10.10.1.1:6121'
```

**Get request using har-caturer**
```bash
chrome-har-capturer --force --port 9222 -o test-quic.har https://www.examplequic.org
```


Use metrics in har file to calculate page load time



# Sources:

1. TownesZhou [CS536-Network-Project](https://github.com/TownesZhou/CS536-Network-Project)
