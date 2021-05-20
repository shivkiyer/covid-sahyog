# Covid-Relief
## For volunteers helping with Covid relief organizations

### Objective of this webapp:
- To create a database of requests and offers for help
- Anonymous users can request or offer help by filling a form
- On submission of the form, an email notification is sent to an email associated with the voluntary organization.
- Volunteers with access to the email can view the details of the request and verify the request by either a phone call or any other means.
- Along with verification, emails of other volunteers can also be entered in the verification form to send notifications about the request or offer.
- Any change to a verified request or offer will trigger an email notification to the admin email and specified volunteer emails.

### Tech stack
- Python3/Django3 in the backend
- Postgresql as database (Sqlite can be used in local dev)
- HTML/Bootstrap/Javascript in the frontend

### How to use this project.
- For local development
  - Install Django 3
  - Check env-sample.py for list of variables
  - Create env.py file and create a SECRET_KEY. Use any other Django project.
  - Create HOSTS=127.0.0.1
  - DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD not needed in development.
  - EMAIL_HOST_USER is an email that you have access to. Go to Gmail settings and turn on less secure app access. (Emails will not be sent unless this access is turned on.)
  - EMAIL_HOST_PASSWORD is the email password.
  - EMAIL_ADMIN_NOTIFICATION is the email to which every email notification should be sent. Can be the same or different from EMAIL_HOST_USER.
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py runserver

- For production
  - Install requirements - pip install requirements.txt
  - Create env.py file and enter all email related variables described in development section above.
  - Installation of mysqlclient or postgresql might fail depending on your machine. Google search. Typical problems - need python-dev, libmariadbclient-dev, libpq-dev installed. These dependencies are OS dependent and on Windows may be very different.
  - Setup a Postgresql server. Create a database, user with write privileges on the database.
  - DB_NAME will be the name of the database, DB_HOST will be the domain name of the server, DB_PORT will usually be 5432 for Postgresql. DB_USER and DB_PASSWORD are the username and password of the user.
  - These variables need to be entered in env.py file (check env-sample.py).
  - If using Heroku for deployment, set all variables in env-sample.py file as environment variables.
  - In Heroku, set DJANGO_SETTINGS_MODULE to be covidapp.settings.production.
  - On a Linux machine, export DJANGO_SETTINGS_MODULE=covidapp.settings.production.
