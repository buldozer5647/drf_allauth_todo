## Setting up a project (on Windows)
1. Virtual environment
```
python -m venv env
env\Scripts\activate
pip install -r requirements
```

2. Running the server
```
cd todoapp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

3. Set up Google Project

On the [Google Developer Console](https://console.cloud.google.com/) you should create a project that authenticates and redirects the user after the login. After that you receive Client ID and Client Secret credentials which are essentinal for Google authentication. Then in admin panel in Sites model you should change `example.com` to `127.0.0.1:8000`and in Socail Application model add an instance with the credentials. In order to not writing a whole page of detailed explanation I leave the helpful links:
- https://www.rootstrap.com/blog/how-to-integrate-google-login-in-your-django-rest-api-using-the-dj-rest-auth-library
- https://dj-rest-auth.readthedocs.io/en/latest/installation.html#google
- https://medium.com/@azubuinedaniel05/using-dj-rest-auth-for-social-logins-with-drf-in-2023-a09b26ad6ee7

After obtaining the credentials create the .env file in the todoapp folder and write them into it like this:
```
CLIENT_ID=<client_id>
CLIENT_SECRET=<client_secret>
```

To create a django admin user, write a command:
```
python manage.py createsuperuser
```
Admin panel can be found on http://127.0.0.1:8000/admin/.

4. Endpoints:
- tasks/: 
  - GET: the list of all authorized user's todo items. You can filter data  in the uri by "complete" and "due_date" fields. Also data is paginated by 12 instances per page. 
  - POST: create a new todo item.
- tasks/*integer_id*/: 
  - GET: information about the single todo item by its id. 
  - PATCH: update the todo item by its id. 
  - DELETE: delete the to do item by its id
- dj-rest-auth/login/ - log in to a website
- dj-rest-auth/registration/ - register a user by email
- dj-rest-auth/google/login - login by Google providing an Access token. In order to have one, you should with the link
`https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<CALLBACK_URL_YOU_SET_ON_GOOGLE>&prompt=consent&response_type=token&client_id=<YOUR CLIENT ID>&scope=openid%20email%20profile`

where: 
- CALLBACK_URL_YOU_SET_ON_GOOGLE is the url as you set up on Google Project and in todoapp/todoapp/views.py in callback_url variable and in get_redirect_url function (I used `http://127.0.0.1:8000/dj-rest-auth/google/login`)
- YOUR CLIENT ID is the credential you received on the Google Developer Console.

After a successful sign in in the url you'l receive an access token which you should send via POST request to dj-rest-auth/google/login/.

5. Running tests.

When you are done with the steps above you can run the tests by the command:
```
python manage.py test
```
Observe tests in the todoapp/tasks/tests.py file.
