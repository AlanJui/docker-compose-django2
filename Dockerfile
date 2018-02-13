FROM    python:3.6

ENV     PYTHONUNBUFFERED 1
RUN     mkdir /app
WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
ADD     requirements.txt /app/
RUN     pip install -r requirements.txt

# Now copy in our code, and run it
ADD     . /app/
#EXPOSE  8000
#CMD     ["python", "manage.py", "runserver", "0.0.0.0:8000"]