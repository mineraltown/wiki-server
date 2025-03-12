# wiki-server

## 部署

```sh
pip install django-cors-headers
pip install django-tinymce
pip install "psycopg[binary]"
```

```sh
# 创建项目
mkdir wiki-server
django-admin startproject wiki wiki-server
# 创建应用
python manage.py startapp index
# 检测对模型文件的修改
python manage.py makemigrations
# 在数据库中创建表
python manage.py migrate
# 创建管理员账号
python manage.py createsuperuser
# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

## settings.py

```py
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    'tinymce',
    ...
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "wiki",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"
```
