# mineraltown.net
# Debian 13 Trixie

# 更新软件源
apt update && apt upgrade -y && apt autoremove -y

# 设置系统时区为 亚洲/上海
dpkg-reconfigure tzdata

# 设置系统语言为 zh_CN.UTF-8
dpkg-reconfigure locales
locale-gen zh_CN.UTF-8

# 创建用户
adduser wiki
usermod -aG sudo wiki
# echo "wiki ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers

# 设置主机名称
echo "MineralTown" > /etc/hostname
hostname -F /etc/hostname

# 登录信息
cat /dev/null > /etc/motd
sed -i "s/uname/# uname/g" /etc/update-motd.d/10-uname
cp 99-panel /etc/update-motd.d/

# C & C++
# apt install -y build-essential cmake

# Python3
apt install -y python3 python3-dev python3-pip python3-venv
update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Git
apt install -y git wget curl
ssh-keygen -t ed25519  -N "" -C "Mineraltown"

# Vim
apt install -y vim exuberant-ctags
git clone --depth=1 https://github.com/MisakaAI/vim-config.git
cd vim-config
bash ./install.sh
cd ..
rm -r vim-config

# 防止 SSH 自动断开
sed -i "s/#TCPKeepAlive yes/TCPKeepAlive yes\nClientAliveInterval 60\nClientAliveCountMax 120/g" /etc/ssh/sshd_config

# 禁止 root 用户登录
sed -i "s/PermitRootLogin yes/PermitRootLogin no/g" /etc/ssh/sshd_config

# 禁止使用密码登录
sed -i 's/^#\?PasswordAuthentication[[:space:]].*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 更改 SSH 默认端口
while true; do
    read -p "请输入 SSH 端口 (1000-65535): " port

    # 如果为空 → 默认 22
    if [ -z "$port" ]; then
        port=22
        echo "使用默认端口: 22"
        break
    fi

    # 判断是否是纯数字
    if ! [[ "$port" =~ ^[0-9]+$ ]]; then
        echo "请输入数字"
        continue
    fi

    # 判断范围
    if [ "$port" -lt 1000 ] || [ "$port" -gt 65535 ]; then
        echo "端口必须在 1000-65535 之间"
        continue
    fi

    break
done

sed -i "s/^#Port 22/Port $port/" /etc/ssh/sshd_config
echo "SSH 端口已修改为: $port"

# 重启 SSH 服务
systemctl restart ssh.service

# Zsh
apt install -y zsh zsh-syntax-highlighting
sh -c 'echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> /etc/zsh/zshrc'
sh -c 'echo "setopt no_nomatch" >> /etc/zsh/zshrc'
sh -c 'echo "zstyle \":completion:*\" rehash true" >> /etc/zsh/zshrc'

# Oh My ZSH
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
omz theme set ys

# 其他常用
apt install -y fastfetch htop tmux screen
apt install -y nmap zip unzip zstd

# 查看是否启用 BBR
lsmod | grep bbr

# Nginx
# https://nginx.org/en/linux_packages.html#Debian

# 安装依赖
apt-get update
sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring

# 导入官方的nginx签名密钥，以便apt可以验证软件包的真实性。
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

# 验证下载的文件是否包含正确的密钥
# 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
# mkdir -p ~/.gnupg
# chmod 700 ~/.gnupg
# gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg

# 使用稳定版的 Nginx 存储库
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

# 安装 Nginx
sudo apt update
sudo apt install nginx
systemctl enable --now nginx.service
systemctl status nginx.service

chown -R www-data:www-data /var/log/nginx

# 生成 dhparam 文件
# openssl dhparam -out /etc/nginx/dhparam 2048
curl https://ssl-config.mozilla.org/ffdhe2048.txt > /etc/nginx/dhparam

# Nginx 复制配置文件
cp -rf nginx/* /etc/nginx

# PostgreSQL
# https://www.postgresql.org/download/linux/debian/
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt update
sudo apt install postgresql-18
systemctl enable --now postgresql.service

su postgres
pgsql   # \password
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres

echo -e "请输入 PostgreSQL 密码:"
read -r -s PG_PASSWD
echo -e "\n"
echo "*:5432:*:postgres:$PG_PASSWD" > ~/.pgpass
chmod 600 ~/.pgpass

# PostgreSQL 公网访问
# 不再配置公网访问，使用 ssh 隧道进行备份
# vim /etc/postgresql/18/main/postgresql.conf
# listen_addresses = '*'
# vim /etc/postgresql/18/main/pg_hba.conf
# host    all             all             0.0.0.0/0          scram-sha-256

# 重启 PostgreSQL 服务
systemctl restart postgresql.service

# Redis
apt install -y redis-server
systemctl enable --now redis-server.service
usermod -aG redis misaka
usermod -aG redis www-data

# vim /etc/redis/redis.conf
echo "
unixsocket /run/redis/redis-server.sock
unixsocketperm 770
maxmemory-policy allkeys-lru
# allkeys-lru : 删旧数据，保证新写入成功
# noeviction : 不删数据，新写入直接报错
"

# 重启 Redis 服务
systemctl restart redis-server.service

# crontab
apt install -y cron
systemctl enable --now cron

# ACME
# https://github.com/acmesh-official/acme.sh/wiki/How-to-install
curl https://get.acme.sh | sh -s email=friends@mineraltown.net
cd ~/.acme.sh/
export CF_Token=""
export CF_Account_ID=""

./acme.sh --issue --dns dns_cf -d mineraltown.net -d '*.mineraltown.net'

mkdir /etc/ssl/mineraltown.net
~/.acme.sh/acme.sh --install-cert -d mineraltown.net \
    --key-file       /etc/ssl/mineraltown.net/privkey.pem  \
    --fullchain-file /etc/ssl/mineraltown.net/fullchain.pem \
    --reloadcmd     "systemctl force-reload nginx.service"

systemctl restart nginx.service

# wiki
git clone -b reborn git@github.com:mineraltown/wiki.git /var/www/wiki
git config --global --add safe.directory /var/www/wiki

# wiki-server & Django
mkdir -p /var/www/wiki-server
git clone git@github.com:mineraltown/wiki-server.git /var/www/wiki-server
git config --global --add safe.directory /var/www/wiki-server

cd /var/www/wiki-server
python3 -m venv .venv
source .venv/bin/activate
which pip
pip install -r requirements.txt

chown -R www-data:www-data /var/www/wiki-server

# uwsgi
echo "[uwsgi]
chdir=/var/www/wiki-server
uid=www-data
gid=www-data
module=wiki.wsgi:application
master=True
home=/var/www/wiki-server/.venv
processes=2
threads=4
vacuum=True
logto=/var/log/uwsgi/wiki.log
log-maxsize = 10000
max-requests = 5000
pidfile=/tmp/uwsgi_wiki.pid
socket=/var/www/wiki-server/wiki.sock" > /var/www/wiki-server/uwsgi.ini

mkdir -p /var/log/uwsgi
chown -R www-data:www-data /var/log/uwsgi

# mv ~misaka/settings.py /var/www/wiki-server/wiki
zstd -d wiki.sql.zst
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -c "CREATE DATABASE wiki;"
psql -U postgres -h 127.0.0.1 -p 5432 -d postgres -f wiki.sql

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

# Systemd
echo "[Unit]
Description=uWSGI wiki
After=syslog.target

[Service]
User=www-data
Group=www-data
ExecStart=/var/www/wiki-server/.venv/bin/uwsgi --ini /var/www/wiki-server/uwsgi.ini
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/wiki.service

systemctl enable --now wiki.service
systemctl status wiki.service

# Fail2Ban
# 锦上添花，已经禁止 root 登录和密码登录，很安全了。
apt install -y fail2ban
echo "
[DEFAULT]
# 是否允许 IPv6 地址。
# 默认值是 auto，表示自动检测。
allowipv6 = auto
# 查找时间：在这个时间段内超过最大失败尝试次数会被封禁，单位是秒。
# 3600 秒 = 1 小时
findtime = 3600
# 最大失败尝试次数：在查找时间段内允许的最大失败尝试次数。
maxretry = 3
# 白名单
# ignoreip = 127.0.0.1/8
# 封禁动作
banaction = nftables
# 禁止时间：被封禁 IP 地址的时长，单位是秒。
# 1 Day = 1 天
bantime  = 1d
# 开启递增封禁
bantime.increment = true
# 递增倍率（指数增长系数）
bantime.factor = 2
# 封禁时间上限
bantime.max = 7d
[sshd]
# 是否启用此 jail。true 表示启用，false 表示禁用。
enabled  = true
# 指定使用的过滤器。
# fail2ban 将使用这个过滤器从日志中提取失败的 SSH 登录尝试。
filter = sshd
# 监听的端口。默认是 ssh，可以根据需要修改。
port     = 2333
# 日志文件的后端。使用 systemd 来读取 journald 日志。
backend = systemd
" > /etc/fail2ban/jail.local
systemctl restart fail2ban.service
fail2ban-client status sshd
