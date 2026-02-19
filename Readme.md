# How to setup development environment
1. import dependencies `pip install -r requirements.txt`
2. move to django directory `cd DjangoFramework`
3. apply migrations for django database `python manage.py migrate`
4. import static data into database:
    1. import missions  `python manage.py runscript gamification.import_data`
    2. import passports `python manage.py runscript passport.import_product_data`
## How to run
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