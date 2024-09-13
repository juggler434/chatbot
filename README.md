# chatbot
A not very smart chatbot

To run locally you need to set some environment variables.  This project supports using a .env file.
Heres an example of what they would look like:
SQLALCHEMY_DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/chatbot"
AUTH_SECRET_KEY="35e9143ec2bbce516dfc904ca604eafbf299a7f407a84c6ca5a3925b9bef416b"
AUTH_ALGORITHM="HS256"

Set up a Postgres DB and use alembic to run the migrations
