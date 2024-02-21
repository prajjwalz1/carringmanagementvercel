 echo "BUILD START"
 # python3.9 -m pip install -r requirements.txt
 python3.9 -m venv venv
    source venv/bin/activate
 pip install -r requirements.txt
 # python3.9 manage.py collectstatic
 # ls
 echo "BUILD END"
# source venv/bin/activate

 # Collect static files
echo "Collecting static files..."
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
