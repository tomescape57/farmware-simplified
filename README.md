This project is for developing a inventory management system.
For study and connect to industry skills.



test operation steps:
set up python
sudo apt install python3 python3-pip python3-venv
create virtual python environment(protect global lib)
python3 -m venv venv

active virtual python environment
source venv/bin/activate
exit: deactive

install dependencies:
!!!change global python lib source to qing hua !!!
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple 

pip install fastapi uvicorn[standard] sqlalchemy python-dotenv passlib[bcrypt] python-jose[cryptography] pydantic

Run (under venv!):
python3 -m uvicorn app.main:app --reload

changed my email sep22 26.


=== before run ===
# venv
sudo apt install python3-venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate


pip install uvicorn fastapi sqlalchemy
pip install passlib bcrypt
pip install email-validator
pip install PyJWT

=== RUN ===
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload