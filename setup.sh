sudo apt update && sudo apt upgrade -y
sudo apt intall python3.12-env -y
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt