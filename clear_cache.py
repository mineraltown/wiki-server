# 清空缓存

'''redis
# 连接数据库
redis-cli -s /run/redis/redis-server.sock

# 清空数据库
FLUSHDB

# 清空所有数据库
FLUSHALL
'''

import os
import django
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki.settings")
django.setup()
cache.clear()
