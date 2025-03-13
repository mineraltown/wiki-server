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
# 创建应用 主页
python manage.py startapp index
# 检测对模型文件的修改
python manage.py makemigrations
# 在数据库中创建表
python manage.py migrate
# 创建管理员账号
python manage.py createsuperuser
# 启动开发服务器
python manage.py runserver 0.0.0.0:8888

# 创建应用 重聚矿石镇
python manage.py startapp saikai
```

## settings.py

```py
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    ...
    "index.apps.IndexConfig",
    "saikai.apps.SaikaiConfig",
    'tinymce',
    "corsheaders",
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
USE_TZ = False

STATIC_URL = "static/"
STATIC_ROOT = "static/"
MEDIA_ROOT = "media/"
MEDIA_URL = "media/"

CORS_ALLOW_ALL_ORIGINS = True
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]

TINYMCE_DEFAULT_CONFIG = {
    "height": 800,
    "width": 1200,
    "menubar": True,
    "language": "zh-Hans",
    "plugins": "anchor link autolink code charmap emoticons fullscreen"
    "help image lists advlist preview table visualblocks visualchars wordcount",
    "toolbar": "undo redo | fontsize styles | "
    "bold italic underline |  forecolor backcolor | "
    "table visualblocks visualchars | bullist numlist | "
    "searchreplace  | link image | code preview | fullscreen help",
}
```
