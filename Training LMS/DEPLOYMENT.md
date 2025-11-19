# SmartIce LMS 部署文档

本文档提供SmartIce培训管理系统的完整部署指南，包括开发环境、生产环境（Docker）和传统部署方式。

---

## 目录

1. [系统要求](#系统要求)
2. [快速开始（开发环境）](#快速开始开发环境)
3. [Docker部署（推荐）](#docker部署推荐)
4. [传统部署（手动）](#传统部署手动)
5. [数据库迁移](#数据库迁移)
6. [环境变量配置](#环境变量配置)
7. [安全加固](#安全加固)
8. [监控与维护](#监控与维护)
9. [故障排查](#故障排查)

---

## 系统要求

### 最低配置
- **CPU**: 2核心
- **内存**: 4GB RAM
- **硬盘**: 20GB可用空间
- **操作系统**: Linux (Ubuntu 20.04+) / macOS / Windows

### 推荐配置
- **CPU**: 4核心
- **内存**: 8GB RAM
- **硬盘**: 50GB SSD
- **操作系统**: Ubuntu 22.04 LTS

### 软件依赖

**开发环境**:
- Python 3.9+
- Node.js 18+
- SQLite 3

**生产环境**:
- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 15+ (如不使用Docker)

---

## 快速开始（开发环境）

### 1. 克隆项目

```bash
git clone https://github.com/YukikoYoung/smartice-training-lms.git
cd smartice-training-lms
```

### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库和示例数据
python3 scripts/init_data.py
python3 scripts/init_courses.py

# 生成题库（556道题）
python3 scripts/generate_front_batch3_questions.py
python3 scripts/generate_kitchen_batch3_questions.py
python3 scripts/generate_comprehensive_questions.py

# 启动后端（开发模式）
python3 main.py
```

后端将运行在 `http://localhost:8000`，API文档：`http://localhost:8000/docs`

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 `http://localhost:5173`

### 4. 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| store_mgr | 123456 | 店长 |
| waiter001 | 123456 | 服务员 |

---

## Docker部署（推荐）

### 1. 准备工作

确保已安装Docker和Docker Compose：

```bash
# 检查Docker版本
docker --version  # 需要 20.10+
docker-compose --version  # 需要 2.0+
```

### 2. 配置环境变量

复制环境变量模板并修改配置：

```bash
cp .env.example .env
nano .env  # 或使用其他编辑器
```

**关键配置（必须修改）**:
```bash
# 数据库密码（生产环境必改）
DB_PASSWORD=your_secure_password

# JWT密钥（生产环境必改，使用随机字符串）
SECRET_KEY=your_random_secret_key_here

# CORS域名（改为实际域名）
CORS_ORIGINS=https://your-domain.com
```

生成安全的SECRET_KEY：
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 构建和启动

```bash
# 构建镜像（首次或代码更新后）
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据

```bash
# 进入后端容器
docker-compose exec backend bash

# 初始化数据
python3 scripts/init_data.py
python3 scripts/init_courses.py

# 生成题库
python3 scripts/generate_front_batch3_questions.py
python3 scripts/generate_kitchen_batch3_questions.py
python3 scripts/generate_comprehensive_questions.py

# 退出容器
exit
```

### 5. 访问系统

- **前端**: `http://localhost` (端口80)
- **后端API**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs`

### 6. 常用Docker命令

```bash
# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（⚠️ 会清空数据库）
docker-compose down -v

# 查看日志
docker-compose logs backend  # 后端日志
docker-compose logs frontend  # 前端日志
docker-compose logs db  # 数据库日志

# 进入容器
docker-compose exec backend bash
docker-compose exec db psql -U smartice -d training_lms
```

---

## 传统部署（手动）

### 1. 后端部署

#### 安装PostgreSQL

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**创建数据库**:
```bash
sudo -u postgres psql

CREATE DATABASE training_lms;
CREATE USER smartice WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE training_lms TO smartice;
\q
```

#### 部署后端应用

```bash
# 创建应用目录
sudo mkdir -p /opt/smartice-lms/backend
cd /opt/smartice-lms/backend

# 复制代码
cp -r /path/to/your/backend/* .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cat > .env << EOF
DATABASE_URL=postgresql://smartice:your_password@localhost/training_lms
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
DEBUG=false
EOF

# 初始化数据
python3 scripts/init_data.py
python3 scripts/init_courses.py

# 生成题库
python3 scripts/generate_front_batch3_questions.py
python3 scripts/generate_kitchen_batch3_questions.py
python3 scripts/generate_comprehensive_questions.py
```

#### 配置Systemd服务

创建 `/etc/systemd/system/smartice-lms.service`:

```ini
[Unit]
Description=SmartIce LMS Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/smartice-lms/backend
Environment="PATH=/opt/smartice-lms/backend/venv/bin"
ExecStart=/opt/smartice-lms/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start smartice-lms
sudo systemctl enable smartice-lms
sudo systemctl status smartice-lms
```

### 2. 前端部署

#### 构建前端

```bash
cd /opt/smartice-lms/frontend
npm install
npm run build
```

#### 配置Nginx

安装Nginx：
```bash
sudo apt install nginx
```

创建 `/etc/nginx/sites-available/smartice-lms`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    root /opt/smartice-lms/frontend/dist;
    index index.html;

    # Gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/smartice-lms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 配置HTTPS（可选但推荐）

使用Let's Encrypt：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 数据库迁移

### SQLite → PostgreSQL

如果从开发环境（SQLite）迁移到生产环境（PostgreSQL）：

#### 方法1：重新初始化（推荐）

```bash
# 1. 配置PostgreSQL连接
export DATABASE_URL=postgresql://user:pass@localhost/training_lms

# 2. 运行应用自动创建表
python3 main.py  # 会自动创建所有表

# 3. 初始化数据
python3 scripts/init_data.py
python3 scripts/init_courses.py
python3 scripts/generate_*.py  # 生成题库
```

#### 方法2：数据迁移（保留现有数据）

使用pgloader工具：
```bash
sudo apt install pgloader

pgloader sqlite:///path/to/training_lms.db \
  postgresql://user:pass@localhost/training_lms
```

### 备份与恢复

#### PostgreSQL备份

```bash
# 备份数据库
pg_dump -U smartice training_lms > backup_$(date +%Y%m%d).sql

# 压缩备份
gzip backup_$(date +%Y%m%d).sql
```

#### PostgreSQL恢复

```bash
# 恢复数据库
psql -U smartice training_lms < backup_20250115.sql
```

#### Docker环境备份

```bash
# 备份PostgreSQL数据
docker-compose exec db pg_dump -U smartice training_lms > backup.sql

# 恢复数据
docker-compose exec -T db psql -U smartice training_lms < backup.sql
```

---

## 环境变量配置

### 完整环境变量列表

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `DATABASE_URL` | 数据库连接URL | SQLite | 生产必填 |
| `SECRET_KEY` | JWT签名密钥 | - | ✅ 必填 |
| `ALGORITHM` | JWT算法 | HS256 | 否 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token有效期（分钟） | 1440 | 否 |
| `APP_NAME` | 应用名称 | SmartIce LMS | 否 |
| `DEBUG` | 调试模式 | false | 否 |
| `CORS_ORIGINS` | 允许的跨域源 | localhost | 生产必填 |
| `DB_USER` | 数据库用户名 | smartice | Docker必填 |
| `DB_PASSWORD` | 数据库密码 | smartice123 | ✅ 必填 |
| `DB_NAME` | 数据库名称 | training_lms | 否 |
| `BACKEND_PORT` | 后端端口 | 8000 | 否 |
| `FRONTEND_PORT` | 前端端口 | 80 | 否 |

### 开发环境配置

```bash
DATABASE_URL=sqlite:///./training_lms.db
SECRET_KEY=dev_secret_key_change_in_production
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 生产环境配置

```bash
DATABASE_URL=postgresql://user:password@db-host:5432/training_lms
SECRET_KEY=<使用随机生成的64字符密钥>
DEBUG=false
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 安全加固

### 1. 数据库安全

- ✅ 修改默认数据库密码
- ✅ 限制数据库远程访问（仅localhost）
- ✅ 定期备份数据库
- ✅ 使用连接池限制并发连接数

**PostgreSQL配置** (`/etc/postgresql/*/main/pg_hba.conf`):
```
# 仅允许本地连接
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
```

### 2. 应用安全

- ✅ 使用HTTPS（Let's Encrypt免费SSL证书）
- ✅ 配置CORS白名单（只允许合法域名）
- ✅ 修改默认管理员密码
- ✅ 定期更新依赖包
- ✅ 限制文件上传大小
- ✅ 实施速率限制防止暴力破解

### 3. 服务器安全

- ✅ 关闭不必要的端口（使用防火墙）
- ✅ 配置fail2ban防止SSH暴力破解
- ✅ 定期更新系统补丁
- ✅ 使用非root用户运行应用

**UFW防火墙配置**:
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 4. 密钥管理

**生成强随机密钥**:
```bash
# SECRET_KEY (32字节)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 数据库密码 (16字节)
python3 -c "import secrets; print(secrets.token_urlsafe(16))"
```

**环境变量安全存储**:
- 使用`.env`文件（不提交到Git）
- 文件权限：`chmod 600 .env`
- 生产环境使用密钥管理服务（如AWS Secrets Manager、HashiCorp Vault）

---

## 监控与维护

### 1. 日志管理

**后端日志**:
```bash
# Docker环境
docker-compose logs -f --tail=100 backend

# 传统部署
journalctl -u smartice-lms -f
```

**Nginx访问日志**:
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 性能监控

**数据库性能**:
```sql
-- 查看慢查询
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- 查看活跃连接
SELECT * FROM pg_stat_activity;
```

**系统资源**:
```bash
# CPU和内存使用
htop

# 磁盘使用
df -h

# Docker容器资源
docker stats
```

### 3. 定期维护任务

**每日任务**:
- 数据库备份
- 日志轮转

**每周任务**:
- 检查系统更新
- 审查错误日志
- 磁盘空间清理

**每月任务**:
- 安全补丁更新
- 性能优化分析
- 备份数据验证

### 4. 自动化备份脚本

创建 `/opt/scripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR=/opt/backups
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T db pg_dump -U smartice training_lms > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql

# 保留最近30天的备份
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: db_$DATE.sql.gz"
```

添加到crontab：
```bash
# 每天凌晨2点自动备份
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

---

## 故障排查

### 常见问题

#### 1. 后端无法启动

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

**错误**: `FATAL: database "training_lms" does not exist`

**解决**:
```bash
# 创建数据库
createdb -U smartice training_lms

# 或使用psql
psql -U postgres
CREATE DATABASE training_lms;
```

#### 2. 前端无法访问后端API

**错误**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**解决**:
- 检查`CORS_ORIGINS`环境变量是否包含前端域名
- 确保后端CORS中间件配置正确

#### 3. Docker容器无法启动

**错误**: `port is already allocated`

**解决**:
```bash
# 查看端口占用
lsof -i :8000

# 修改端口（.env文件）
BACKEND_PORT=8001
```

**错误**: `health check failed`

**解决**:
```bash
# 查看容器日志
docker-compose logs backend

# 进入容器检查
docker-compose exec backend bash
curl http://localhost:8000/health
```

#### 4. 数据库连接失败

**错误**: `could not connect to server`

**解决**:
```bash
# 检查PostgreSQL服务状态
sudo systemctl status postgresql

# 检查网络连接
docker-compose exec backend ping db

# 查看数据库日志
docker-compose logs db
```

### 健康检查

#### 系统健康检查脚本

```bash
#!/bin/bash

echo "=== SmartIce LMS 健康检查 ==="

# 1. 检查后端服务
echo -n "后端服务: "
curl -s http://localhost:8000/health | grep -q "healthy" && echo "✅ 正常" || echo "❌ 异常"

# 2. 检查前端服务
echo -n "前端服务: "
curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200" && echo "✅ 正常" || echo "❌ 异常"

# 3. 检查数据库连接
echo -n "数据库连接: "
docker-compose exec -T db pg_isready -U smartice && echo "✅ 正常" || echo "❌ 异常"

# 4. 检查磁盘空间
echo -n "磁盘空间: "
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo "✅ 正常 (${DISK_USAGE}%)"
else
    echo "⚠️ 警告 (${DISK_USAGE}%)"
fi

# 5. 检查内存使用
echo -n "内存使用: "
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEM_USAGE -lt 90 ]; then
    echo "✅ 正常 (${MEM_USAGE}%)"
else
    echo "⚠️ 警告 (${MEM_USAGE}%)"
fi

echo "======================"
```

---

## 附录

### A. 端口列表

| 服务 | 端口 | 协议 | 说明 |
|------|------|------|------|
| 前端 | 80 | HTTP | Nginx |
| 后端API | 8000 | HTTP | FastAPI |
| PostgreSQL | 5432 | TCP | 数据库 |
| HTTPS (可选) | 443 | HTTPS | SSL加密 |

### B. 目录结构

```
/opt/smartice-lms/
├── backend/           # 后端应用
│   ├── app/          # 应用代码
│   ├── venv/         # Python虚拟环境
│   ├── data/         # 数据目录
│   └── logs/         # 日志文件
├── frontend/         # 前端应用
│   └── dist/         # 构建输出
├── backups/          # 数据库备份
└── scripts/          # 维护脚本
```

### C. 性能优化建议

1. **数据库优化**
   - 为常查询字段添加索引
   - 使用连接池（SQLAlchemy已内置）
   - 定期执行`VACUUM`清理

2. **前端优化**
   - 启用Gzip压缩
   - 配置浏览器缓存
   - 使用CDN加速静态资源

3. **后端优化**
   - 使用Gunicorn多进程部署
   - 配置Redis缓存（可选）
   - 启用数据库查询缓存

### D. 联系方式

- **GitHub Issues**: https://github.com/YukikoYoung/smartice-training-lms/issues
- **文档**: https://github.com/YukikoYoung/smartice-training-lms

---

**版本**: 1.0.0
**更新日期**: 2025-01-15
**维护者**: SmartIce Team
