# 如何操作使用

## 使用非 PyCharm IDE

1. 進入「工作區」目錄

```
cd ~/workspace/docker
```

2.  自 GitHub 下載

```
git clone git@github.com:AlanJui/docker-compose-django2.git
```

3. 進入「專案」目錄

```
cd docker-compse-django2
```

4. 建立 Web Serive 所需使用之 Docker Image

```
docker-compose build
```

【驗證】：

```
$ docker images
REPOSITORY                               TAG                 IMAGE ID            CREATED              SIZE
dockercomposedjango2_web                 latest              f5c409ac0b59        About a minute ago   742MB
python                                   3.6                 336d482502ab        3 days ago           692MB
djangoapp01_web                          latest              eedf429c1486        7 days ago           737MB
```




5. 啟動專案待開發之「應用系統」（以下簡稱： App ）


```
docker-compose up
```

【驗證】：

```
$ docker-compose ps
           Name                         Command               State           Ports
--------------------------------------------------------------------------------------------
dockercomposedjango2_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
dockercomposedjango2_web_1   python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp
```

```
$ docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                    NAMES
e15fcfa4a19e        dockercomposedjango2_web   "python manage.py ru…"   2 minutes ago       Up 2 minutes        0.0.0.0:8000->8000/tcp   dockercomposedjango2_web_1
33448f8b051c        postgres:9.6               "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        0.0.0.0:5432->5432/tcp   dockercomposedjango2_db_1
```


```
$ docker images
REPOSITORY                               TAG                 IMAGE ID            CREATED             SIZE
dockercomposedjango2_web                 latest              f5c409ac0b59        15 minutes ago      742MB
python                                   3.6                 336d482502ab        3 days ago          692MB
postgres                                 9.6                 c7cca23b4760        4 days ago          266MB
doc
...
```



```
$ docker network ls
NETWORK ID          NAME                                  DRIVER              SCOPE
c3853321ec56        bridge                                bridge              local
ee0a097f4338        dcflask_default                       bridge              local
fee533d364d1        djangoapp01_backend                   bridge              local
490d474748e9        djangoapp01_default                   bridge              local
cc5ce7c738b3        dockercomposedjango2_default          bridge              local
4d761ddc77d9        dockerdevworkflowexpress_backend      bridge              local
```

```
$ docker volume ls
DRIVER              VOLUME NAME
local               0e74874360ecd5e78d41262b76997726c009ec3da47b3bc2ef08863df02ee607
...
local               dockercomposedjango2_db-data
...
```

6. 瀏覽 App 輸出內容。

```
http://127.0.0.1:8000/
```

```
Page not found (404)
Request Method:	GET
Request URL:	http://127.0.0.1:8000/
Using the URLconf defined in web_site.urls, Django tried these URL patterns, in this order:

admin/
hello/
api/members/
The empty path didn't match any of these.

You're seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
```


7. 初始資料庫。

```bash
$ docker-compose exec web python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, members, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying members.0001_initial... OK
  Applying sessions.0001_initial... OK
```

8. 建立資料庫管理使用者帳號。

```
$ docker-compose exec web python manage.py createsuperuser
Username (leave blank to use 'root'): alanjui
Email address: alanjui.1960@gmail.com
Password:
Password (again):
Superuser created successfully.
```


9. 進入 App 後台。

```
http://127.0.0.1:8000/admin
```

 - Username:
 - Password:

10. 進入 admin 後台管理主畫面。

11. 新增 Members 資料紀錄。

12. 驗證 RESTful API: GET /api/members/

```
http://127.0.0.1:8000/api/members/
```

## 使用 PyCharm

## Data Sources Detected



## Run/Debug Configurations 新增：「Run Server」

1. 設定 Project interpreter
 Remote Python Intereter

```
Preferences / Project: docker-compose-django... / Project Interpreter / 
```


2. 設定 Run Configuration

Run / Edit Configurations...

 - Name: docker-compose-django2 (Run Server)
 - Host: 0.0.0.0 (手工輸入)
 - Port: 8000
 - Python iterpreter: Remote Python 3.6.4 Docker Compose (web at [/Users/AlanJui/workspace/docker/docker-compose-django2/docker-compose.yml]) (手工輸入) 


3. 執行「Run Server」

4. 觀察 docker-compose

```
$ docker-compose ps
           Name                         Command               State           Ports
--------------------------------------------------------------------------------------------
dockercomposedjango2_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
dockercomposedjango2_web_1   python -u /code/manage.py  ...   Up      0.0.0.0:8000->8000/tcp
```

5. 驗證 App 能正常執行。

```
http://127.0.0.1:8000/hello/

http://127.0.0.1:8000/api/members/

```

6. 暫停 App 執行： Stop 'Run Server'

7. 觀察 docker-compose 執行狀態。

 - Web Service 已停
 - DB Service 仍繼續執行中

```
$ docker-compose ps
           Name                         Command                State             Ports
-----------------------------------------------------------------------------------------------
dockercomposedjango2_db_1    docker-entrypoint.sh postgres    Up         0.0.0.0:5432->5432/tcp
dockercomposedjango2_web_1   python -u /code/manage.py  ...   Exit 137
```

8.  終止 App 繼續執行。

```
$ docker-compose down
Stopping dockercomposedjango2_db_1 ... done
Removing dockercomposedjango2_web_1 ... done
Removing dockercomposedjango2_db_1  ... done
Removing network dockercomposedjango2_default
```

確認：
```
$ docker-compose ps
Name   Command   State   Ports
------------------------------
```

## Run/Debug Configurations 新增：「Run Server」

1. 新增 Run/Debug Configurations: Build and Run



2. 執行 Run Configuration: Build and Run

3. 觀察 docker-compose ps

```
$ docker-compose ps
           Name                         Command               State           Ports
--------------------------------------------------------------------------------------------
dockercomposedjango2_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
dockercomposedjango2_web_1   python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp
```

4. 透過 Run Configuration: Build and Run 的 Disconnect 。

不等同：終止 docker-compose 執行。


```

```$ docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                    NAMES
f2d097d1cb35        dockercomposedjango2_web   "python manage.py ru…"   7 minutes ago       Up 7 minutes        0.0.0.0:8000->8000/tcp   dockercomposedjango2_web_1
956aad76282d        postgres:9.6               "docker-entrypoint.s…"   7 minutes ago       Up 7 minutes        0.0.0.0:5432->5432/tcp   dockercomposedjango2_db_1
```


## App Debug with PyCharm

1. 設定 Break Point (中斷點) 。

2. 執行 Debug 'Run Server' 。

3. 在瀏覽器輸入網址： http://127.0.0.1:8000/api/members/

4. 在  PyCharm 的 Debug 工具中觀察。

---

# 加入 Member API 的 CRUD 功能

