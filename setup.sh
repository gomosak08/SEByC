sudo apt update && sudo apt upgrade -y
sudo apt install python3.12-venv -y
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt