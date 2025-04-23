# wiki-server

## 部署

```sh
pip install django-cors-headers
pip install django-tinymce
pip install "psycopg[binary]"
pip install Pillow
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
# 将静态文件收集至独立目录(STATIC_ROOT)
python manage.py collectstatic

# 创建应用 居民
python manage.py startapp resident
# 创建应用 提醒
python manage.py startapp todo
# 创建应用 重聚矿石镇
python manage.py startapp saikai
```

## settings.py

```py
DEBUG = False

ALLOWED_HOSTS = ["api.mineraltown.net"]

INSTALLED_APPS = [
    ...
    "index.apps.IndexConfig",
    "resident.apps.ResidentConfig",
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

# 允许所有域名访问
# CORS_ALLOW_ALL_ORIGINS = True

# 授权进行跨站 HTTP 请求的来源列表
# CORS_ALLOWED_ORIGINS = [
#     "https://api.mineraltown.net",
# ]

# 授权进行跨站 HTTP 请求的来源列表（正则）
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.mineraltown\.net$",
]

# 允许将Cookie包含在跨站点HTTP请求中
CORS_ALLOW_CREDENTIALS = True

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
    "relative_urls": False,
    "remove_script_host": True,
    "plugins": "anchor link autolink code charmap emoticons fullscreen"
    "help image lists advlist preview table visualblocks visualchars wordcount",
    "toolbar": "undo redo | fontsize styles | "
    "bold italic underline |  forecolor backcolor | "
    "table visualblocks visualchars | bullist numlist | "
    "searchreplace  | link image | code preview | fullscreen help",
}
```
