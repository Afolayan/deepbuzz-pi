# deepbuzz-pi

Requirements, on RPi
- install Python3-flask
`sudo apt-get install python3-flask`

- pull code from git

- install PageKite from https://pagekite.net/ 
    - `curl -s https://pagekite.net/pk/ |sudo bash`
    - or run   `./install-pagekite.sh`

- check for website url at `https://afolayanseyi.pagekite.me`
- follow the guide at `https://pagekite.net/support/quickstart/`

Run Jupyter
- jupyter notebook

Run this to activate virtual environment
- python3.7 -m venv venv
- source venv/bin/activate

# sudo systemctl restart deepbuzz

#To run flask on local IP
- enter venv with `source venv/bin/activate`
- flask run --host 0.0.0.0

#check this to get location
https://stackoverflow.com/questions/17704436/getting-map-location-python

# to clear out python process
ps -fA | grep python
sudo kill -9 pid