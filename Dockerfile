FROM    python:3.6

ENV     PYTHONUNBUFFERED 1
RUN     mkdir /code
WORKDIR /code

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
ADD     requirements.txt /code/
RUN     pip install --upgrade pip
RUN     pip install -r /code/requirements.txt

# Now copy in our code, and run it
ADD     . /code/

#EXPOSE  8000
#CMD     ["python", "manage.py", "runserver", "0.0.0.0:8000"]