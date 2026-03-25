#!/bin/bash

# 颜色定义
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'

# 智能检测终端 (防止日志文件出现乱码)
if [ -t 1 ]; then
    :
else
    NC='' RED='' GREEN='' YELLOW='' CYAN=''
fi

# 辅助函数
log_info()    { echo -e "${CYAN}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC}   $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

set -e # 遇到错误立即停止

log_info "正在停止服务..."
systemctl stop wiki.service

log_info "正在更新前端代码..."
cd /var/www/wiki && git pull
chown -R www-data:www-data /var/www/wiki

log_info "正在更新后端代码..."
cd /var/www/wiki-server && git pull
chown -R www-data:www-data /var/www/wiki-server

cd ~
log_success "代码更新完成"

log_info "正在解压数据库备份..."
zstd -d -f wiki.sql.zst

log_warn "即将重置数据库 (DROP & CREATE)..."
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -c "DROP DATABASE IF EXISTS wiki;"
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -c "CREATE DATABASE wiki;"
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -f wiki.sql
log_success "数据库重置完成"

log_info "正在重启服务..."
systemctl start wiki.service
systemctl restart nginx.service
systemctl restart redis-server.service

log_success "=== 更新完成 ==="
