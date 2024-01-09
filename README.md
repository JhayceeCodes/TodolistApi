# TODOLIST API
This is a simple yet powerful TodoList API designed to help you manage your tasks efficiently. Built with Django and Django REST Framework, this API allows you to create, retrieve, update, and delete tasks effortlessly. Whether you are building a personal task management app or integrating task functionalities into a larger project, this API provides a flexible and RESTful solution.


# Features
* Task Operations: Perform CRUD operations on tasks with ease.
* User Authentication: Secure your tasks by associating them with user accounts.
* Filter and Sort: Retrieve tasks based on status, priority, or due date.
* Simple Integration: Quickly integrate the API into your project using the provided endpoints.

# How to run
* First, you need to install the required packages on your machine by running `pip install -r  requirements.txt` while in you are in this project directory  already in your terminal
* The installation should be successful provided you've installed python and pip.
* After successful installation, run migrations in order to setup tables in your database by running `python manage.py migrate` in your terminal
* Now it's time to start the server, simply run `python manage.py runserver` and copy the url provided usually "http://127.0.0.1:8000" except in cases where port is defined e.g "python manage.py runserver 9000" which will start the server on "http://127.0.0.1:9000"

# Available Endpoints
NOTE: all endpoints are  to be prefixed with the domain e.g. "http://127.0.0.1:8000"
## ~AUTHENTICATION
#### contains all endpoints that is used for authenticating users
 > /register/ 

   **METHOD(S) ALLOWED: POST** \
    *[this endpoint accept user's data which must include "email, first_name, last_name and password" and if validated by UserSerializer, creates an instance(account) for such user provided the email hasn't been used for registration before. It also sends an "email verification mail" to user's email upon successful registration]*
    ![Alt text](todolist_register.jpg)
   

> /verify_email/

   **METHOD(S) ALLOWED: POST** \
   *[this endpoint verifies user's email by attempting to decode the token(sent to user's email) passed to it as a parameter...if token is valid, user.is_verified is set to true. ~verification mail sent to user will look like: \
   Hi {username}, please click the link below to verify your account
http://127.0.0.1:8000/auth/verify_email/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzA0MTU3NTIwLCJpYXQiOjE3MDQxNTM5MjB9.itFvVIaT5yqHm4oaf0W4xLUF0I0lBMK77iMiW7kTqbg]*
> /login/

   **METHOD(S) ALLOWED: POST** \
   *[this endpoint allows users who have registered to login using their email and password. If email is found and password is correct, it returns two tokens (access and refresh) which will in turn be used for authorization of user]*\
   ![Alt text](todolist_login.jpg)
> /logout/
  
  **METHOD(S) ALLOWED: POST** \
   *[this endpoint logs user out by deleting the authorization tokens(access and refresh) which are initially stored in the web browser's cookie. With this, user is required to re-login the next time they visit the site]*
> /user/

  **METHOD(S) ALLOWED: GET** \
   *[this endpoint fetches current (authorized) user data]*
   ![Alt text](todolist_user.jpg)
> /refresh/

  **METHOD(S) ALLOWED: POST** \
   *[this endpoint is used generate a new access token provided the refresh token has not expire]*
   ![Alt text](todolist_refresh.jpg)
> /reset_password/

  **METHOD(S) ALLOWED: POST** \
   *[this endpoint is accepts an email as data and if email is found, it sends a password reset link (containing uidb64 and a password reset token) to the email]*
   ![Alt text](todolist_reset_password.jpg)
> /confirm_password_reset/\<uidb64>/\<token>/

  **METHOD(S) ALLOWED: GET** \
   *[this endpoint is used to check if a password reset token is valid or not. ~url should look like this http://127.0.0.1:8000/auth/confirm_password_reset/MTU/c01u86-b1b42f29f3979538b0f6949637d7f2d8/ ]*
> /set_new_password/

  **METHOD(S) ALLOWED: PATCH**  \
   *[this endpoint is used to set a new password for the user whose id is decoded from the uidb64 provided both uidb64 and token are valid...expects three data: password, uidb64, token. request should contain {\
    "password": "your new password",\
    "uidb64": "uidb64",\
    "token": "token"\ 
      } ~uidb64 will be gotten from the reset password link sent to your email]*

## ~TODO
#### contains all endpoints used to perform CRUD operation on tasks 
> /todolists/
  
  **METHOD(S) ALLOWED: GET, POST**  
  *[this endpoint is used to fetch and create todolists for the current user...the GET request fetches all todolists created by the current user while POST request creates a new todolist with the name provided]*
> /todolists/<int:pk>/

  **METHOD(S) ALLOWED: GET, PUT, DELETE**  
  *[this endpoint is used to fetch details of a particular todolist and perform operations like PUT and DELETE, provide the todolist_pk is valid and was created by the current user ]* 
> /todolists/<int:todolist_id>/todos/

  **METHOD(S) ALLOWED: GET, POST**  
  *[this endpoint is used to fetch and create todos for a particular todolist provided todolist exist and was created by the current user]*


> /todolists/<int:todolist_id>/todos/<int:pk>/

  **METHOD(S) ALLOWED: GET, PUT, DELETE**  
  *[this endpoint allows users to fetch details of a particular todo and even update or delete it  ]*
  
##### NOTE : todolists and their todos can only be accessed by users who created them initially otherwise, permission will be denied even if the todolist exists.