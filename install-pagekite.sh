#!/usr/bin/env bash

curl -O https://pagekite.net/pk/pagekite.py
chmod +x pagekite.py
sudo mv -f pagekite.py /usr/local/bin

## run this to start pagekite
## python /usr/local/bin/pagekite.py 5000 afolayanseyi.pagekite.me