python -m venv .venv
. .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd tshirt_shop
python manage.py migrate
python manage.py runserver