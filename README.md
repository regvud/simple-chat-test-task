Current project implements Simple Chat application.


Instruction:

1. Create virtual environment:

python -m venv venv

source venv/bin/activate


2. Install dependencies

pip install -r requirements.txt



3. Ensure that migrations are applied

./manage.py migrate 



4. To use any of endpoints you have to obtain access token and use it as Bearer in requests.

    1) login credentials: { "username": "user1", "password": "user" } 
    (or create new user on endpoint: localhost:8000/users/ with post request)

    2) post request with login credentials on endpoint: localhost:8000/auth/login
    
# simple-chat-test-task
