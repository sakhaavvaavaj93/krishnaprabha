echo "Cloning Repo, Please Wait..."
git clone https://github.com/sakhaavvaavaj93/krishnaprabha.git/ krishnaprabha 
echo "Installing Requirements..."
cd /krishnaprabha
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 main.py
