
# How to run
1. import dependencies `pip install requirements.txt`
2. import data:
    1. import missions  `python manage.py runscript gamification.import_data`
    2. import passports `python manage.py runscript passport.import_product_data`
3. run commands:
```shell
cd DjangoFramework
python manage.py runserver
```
1. open page in browser : http://127.0.0.1:8000/

# How to run tests
1. import dependencies `pip install requirements.txt`
2. run commands:
```shell
cd DjangoFramework
python manage.py test
```

# Notes about accounts current state
1. Files can be found in `/DjangoFramework/Users`
2. accesses account control by going to http://127.0.0.1:8000/accounts

## Temp super user login for testing
Username - Superuser\
Password - Food4thought\
email - zjmf201@exeter.ac.uk   
