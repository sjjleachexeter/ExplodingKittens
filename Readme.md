
# How to run development
1. `cd DjangoFramework`
2. install requirements from `requirements.txt`
3. run  `python manage.py runserver`
4. open page in browser : http://127.0.0.1:8000/

# how to run docker
1. make sure that you have docker and nginx installed on the system
2. `cd DjangoFramework`
3. generate ssl keys and cert.
   1. sign you own keys if you don't have a domain: `openssl req -x509 -nodes -days 365   -newkey rsa:2048   -keyout ./nginx/certs/nginx.key   -out ./nginx/certs/nginx.crt \`
   2. get cert from correct authority and put in the same location
4. create `.env` file :
   ```.dotenv
   SECRET_KEY=<your_secret_key>
   DEBUG=<debug_status>
   DJANGO_ALLOWED_HOST=<your_allowed_host>
   DJANGO_CSRF_TRUSTED_ORIGINS=<your_trusted_origins>
   ```
5. build and run with `docker compose up --build`

