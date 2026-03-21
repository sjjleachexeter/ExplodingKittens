# Requirements
- Docker
# Setup
1. clone / download repository 
2. `cd DjangoFramework`
3. generate ssl keys and cert either:
    1. sign you own keys if you don't have a domain:
       `mkdir nginx/certs &&openssl req -x509 -nodes -days 365   -newkey rsa:2048   -keyout ./nginx/certs/nginx.key   -out ./nginx/certs/nginx.crt \`
    2. get cert from correct authority and put place in `./nginx/certs/` named `nginx.key` and `nginx.crt`
4. create `.env` file as bellow:
   ```.dotenv
   SECRET_KEY=<your_secret_key>
   DEBUG=<debug_status>
   DJANGO_ALLOWED_HOST=<your_allowed_host>
   DJANGO_CSRF_TRUSTED_ORIGINS=<your_trusted_origins>
   ```
# Run
 build and run with `docker compose up --build`

# Seed Datasets
 while container is running:
1. import missions  `docker compose exec django-web python manage.py runscript gamification.import_data`
2. import passports `docker compose exec django-web python manage.py runscript passport.import_product_data`

# Create Superuser
Create a superuser to manage user roles from within the website
1. `docker compose exec django-web python manage.py createsuperuser`
2. follow instructions in command line