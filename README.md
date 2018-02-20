# 專案指引

本專案用於實作可支援 Django 2 + RESTful API 之「專案模版」。

本專案模版之「開發環境」規格如下：

 - 支援 PostgreSQL 資料庫系統
 - 使用 psycopg2 套件存／取資料庫系統 (套件之新名稱應改為： psycopg2-binary )
 - 支援 Docker Compose 
 - 支援 IDE: PyCharm 2017.3
 - 開發人員所使用的 Host 環境可為： Mac OS/X 10.13.3 或 Windows 10

---

# 建立開發環境作業流程

## 建立專案目錄

### 1. 建立專案目錄

```
mkdir docker-compose-django2
```


### 2. 進入專案目錄

```
cd docker-compose-django2
```

## 建立 Docker Compose 設定檔

### 1. requirements.txt

建立 requirements.txt 檔案，並輸入以下內容：

```dockerfile
Django>=1.11,<2.0
psycopg2-binary
```

### 2. Dockerfile

建立  檔案，並輸入以下內容：

```dockerfile
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
```

### 3. docker-compose.yml

```dockerfile
version: '3'

services:

#  db:
#    image: postgres:9.6
#    volumes:
#      - db-data:/var/lib/postgresql/data/
#    ports:
#      - "5432:5432"
#    networks:
#      - backend
#    environment:
#      POSTGRES_PASSWORD: Passw0rd

  web:
    build: .
    command: command: django-admin startproject web_site .
    command: python3 manage.py runserver 0.0.0.0:8000
#    volumes:
#      - .:/app
    ports:
      - "8000:8000"
    networks:
      - backend
#    depends_on:
#      - db


#volumes:
#  db-data:

networks:
  backend:
```

### 4. docker-compose up

```
$ docker-compose up --build
```

### 5. 為 Django 專案設定權限

```bash
$ chown -R $USER:$USER web_site/
$ chown -R $USER:$USER manage.py
```

### 6. 加入 Postgres 資料庫

__/web_site/settings.py__

```python
...
ALLOWED_HOSTS = [
    '*',
]
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My App
    'web_site',
]
...
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'postgres',
       'USER': 'postgres',
       'PASSWORD': 'Passw0rd',
       'HOST': 'db'
   }
}
...

```

### 7. 改 docker-compose.yml

```dockerfile
version: '3'

services:

  db:
    image: postgres:9.6
    volumes:
      - db-data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: Passw0rd

  web:
    build: .
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    networks:
      - backend
    depends_on:
      - db
#    command: django-admin startproject web_site .
    command: python3 manage.py runserver 0.0.0.0:8000


volumes:
  db-data:

networks:
  backend:
```

### 8. 驗證 Web, DB Service 皆已能正常運作

```bash
$ docker-machine env default
$ eval $("C:\Users\AlanJui\bin\docker-machine.exe" env default)
$ docker-compose build
$ docker-compose up
```

# 安裝套件

安裝 Django REST Framework

### 1. Update requirements.txt

```python
...
djangorestframework=3.7.7
```

### 2. Build Docker Image

```docker
docker-compose build
```

### 3. web_site/settings.py

```python
INSTALLED_APPS = [
    ...

    # My Libs
    'rest_framework',

    # My App
    'web_site',
    'members',
]

```

### 4. members/serializers.py

```python
from rest_framework import serializers

from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
```

### 5. members/views.py

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Member
from .serializers import MemberSerializer

# Create your views here.
...

#========================================
# RESTful API
#========================================

class MemberList(APIView):

    def get(self, request):
        member_list = Member.objects.all()
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)
```

### 6. web_site/urls.py

```python
...
from rest_framework.urlpatterns import format_suffix_patterns

...
from members.views import MemberList

urlpatterns = [
    ...
    path('api/members/', MemberList.as_view()),
]
```

---

# 問題排解

## Shared Drives 忘了設定（Docker for Windows）

```dockerfile
$ docker-compose up --build
Building web
Step 1/8 : FROM    python:3.4
3.4: Pulling from library/python
f49cf87b52c1: Already exists
7b491c575b06: Already exists
b313b08bab3b: Already exists
51d6678c3f0e: Already exists
09f35bd58db2: Already exists
3ee016c723da: Pull complete
77694ac69ac6: Pull complete
b0b58499be80: Pull complete
Digest: sha256:777776e8e8cc8d25c0da87bf648bbc51d8e7eb4ef88c434a6e0a5b69b8b910e4
Status: Downloaded newer image for python:3.4
 ---> 4f56ba3c22c1
Step 2/8 : ENV     PYTHONUNBUFFERED 1
 ---> Running in eeb87e084aa2
Removing intermediate container eeb87e084aa2
 ---> 324d6ae070f5
Step 3/8 : RUN     mkdir /code
 ---> Running in a9fc4f22c9fd
Removing intermediate container a9fc4f22c9fd
 ---> 9c8643f182fa
Step 4/8 : WORKDIR /code
Removing intermediate container cfca7c8db4e7
 ---> c2d41d7211c5
Step 5/8 : ADD     requirements.txt /code/
 ---> 5a3305115a3f
Step 6/8 : RUN     pip install --upgrade pip
 ---> Running in 3b5abcbe76cf
Requirement already up-to-date: pip in /usr/local/lib/python3.4/site-packages
Removing intermediate container 3b5abcbe76cf
 ---> f548b3053d92
Step 7/8 : RUN     pip install -r /code/requirements.txt
 ---> Running in d4cb80233b3f
Collecting Django==2.0 (from -r /code/requirements.txt (line 1))
  Downloading Django-2.0-py3-none-any.whl (7.1MB)
Collecting pytz (from Django==2.0->-r /code/requirements.txt (line 1))
  Downloading pytz-2018.3-py2.py3-none-any.whl (509kB)
Installing collected packages: pytz, Django
Successfully installed Django-2.0 pytz-2018.3
Removing intermediate container d4cb80233b3f
 ---> 50554502b666
Step 8/8 : ADD     . /code/
 ---> 4d115356ac69
Successfully built 4d115356ac69
Successfully tagged dcjango01_web:latest
Creating dcjango01_web_1 ... error

ERROR: for dcjango01_web_1  Cannot create container for service web: Drive has not been shared

ERROR: for web  Cannot create container for service web: Drive has not been shared
ERROR: Encountered errors while bringing up the project.
```

## python3: can't open file 'manage.py': [Errno 2] No such file or directory




````dockerfile
AlanJui@WIN-01 MINGW64 /d/Workspace/Docker/dc_jango_01 (master)                  
$ ll                                                                             
total 8                                                                          
-rw-r--r-- 1 AlanJui 197121    0 二月 14 00:42 db.sqlite3                          
-rw-r--r-- 1 AlanJui 197121  543 二月 14 02:26 docker-compose.yml                  
-rw-r--r-- 1 AlanJui 197121  426 二月 14 02:15 Dockerfile                          
-rwxr-xr-x 1 AlanJui 197121  540 二月 14 00:38 manage.py*                          
-rw-r--r-- 1 AlanJui 197121 3241 二月 14 00:41 README.md                           
-rw-r--r-- 1 AlanJui 197121   41 二月 14 01:19 requirements.txt                    
drwxr-xr-x 1 AlanJui 197121    0 二月 14 01:20 web_site/                           
                                                                                 
AlanJui@WIN-01 MINGW64 /d/Workspace/Docker/dc_jango_01 (master)                  
$ chown -R $USER:$USER web_site/                                                 
                                                                                 
AlanJui@WIN-01 MINGW64 /d/Workspace/Docker/dc_jango_01 (master)                  
$ chown -R $USER:$USER manage.py                                                 
                                                                                 
AlanJui@WIN-01 MINGW64 /d/Workspace/Docker/dc_jango_01 (master)                  
$ ll                                                                             
total 8                                                                          
-rw-r--r-- 1 AlanJui 197121    0 二月 14 00:42 db.sqlite3                          
-rw-r--r-- 1 AlanJui 197121  543 二月 14 02:26 docker-compose.yml                  
-rw-r--r-- 1 AlanJui 197121  426 二月 14 02:15 Dockerfile                          
-rwxr-xr-x 1 AlanJui 197121  540 二月 14 00:38 manage.py*                          
-rw-r--r-- 1 AlanJui 197121 3241 二月 14 00:41 README.md                           
-rw-r--r-- 1 AlanJui 197121   41 二月 14 01:19 requirements.txt                    
drwxr-xr-x 1 AlanJui 197121    0 二月 14 01:20 web_site/                           
                                                                                 
````

### Kill Port

```
0.0.0.0:5432 failed: port is already allocated```
```

Error running 'Debug': com.intellij.docker.remote.run.runtime.WrappedInternalServerErrorException: com.github.dockerjava.api.exception.InternalServerErrorException: {"message":"driver failed programming external connectivity on endpoint dcjango01_db_1 (eafcbc011333a2e4cb80a0307b6adbc5b140ab80015fc9b3e36403857536ecc1): Error starting userland proxy: Bind for 0.0.0.0:5432 failed: port is already allocated"}


Step 1
```
Run command-line as an Administrator. Then run the below mention command. type your port number in yourPortNumber
```

netstat -ano | findstr :yourPortNumber

Step 2

Then you execute this command after identify the PID.

```
taskkill /PID typeyourPIDhere /F
```