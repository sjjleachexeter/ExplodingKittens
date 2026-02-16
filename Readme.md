# How to setup development environment
1. import dependencies `pip install -r requirements.txt`
2. move to django directory `cd DjangoFramework`
3. apply migrations for django database `python manage.py migrate`
4. import static data into database:
    1. import missions  `python manage.py runscript gamification.import_data`
    2. import passports `python manage.py runscript passport.import_product_data`
## How to run development environment
1. setup development environment
2. from `DjangoFramework` run development server `python manage.py runserver`
3. open page in browser : http://127.0.0.1:8000/

## How to run tests
1. setup development environment
2. from `DjangoFramework` run `python manage.py test`

## How to create superuser
1. setup development environment
2. from `DjangoFramework` run `python manage.py createsuperuser` and go though superuser creation prompt
3. once setup you can log in on the website and visit `/admin` to get the superuser overview of the database
# how to run docker

1. make sure that you have docker and nginx installed on the system
2. `cd DjangoFramework`
3. generate ssl keys and cert.
    1. sign you own keys if you don't have a domain:
       `mkdir nginx/certs &&openssl req -x509 -nodes -days 365   -newkey rsa:2048   -keyout ./nginx/certs/nginx.key   -out ./nginx/certs/nginx.crt \`
    2. get cert from correct authority and put in the same location
4. create `.env` file :
   ```.dotenv
   SECRET_KEY=<your_secret_key>
   DEBUG=<debug_status>
   DJANGO_ALLOWED_HOST=<your_allowed_host>
   DJANGO_CSRF_TRUSTED_ORIGINS=<your_trusted_origins>
   ```
5. build and run with `docker compose up --build`
6. import static data while container is running:
    1. import missions  `docker compose exec django-web python manage.py runscript gamification.import_data`
    2. import passports `docker compose exec django-web python manage.py runscript passport.import_product_data`
