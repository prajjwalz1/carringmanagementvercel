
 echo "BUILD START"
 python -m pip install psycopg2-binary
 python -m pip install -r requirements.txt
 python manage.py collectstatic --noinput --clear
 echo "BUILD END"