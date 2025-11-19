# SmartIce LMS Docker部署指南

## 📋 配置文件清单

### ✅ 已创建的文件
- `backend/Dockerfile` - 后端Python/FastAPI镜像配置
- `backend/.dockerignore` - 后端构建排除文件
- `frontend/Dockerfile` - 前端React多阶段构建配置
- `frontend/.dockerignore` - 前端构建排除文件
- `frontend/nginx.conf` - Nginx反向代理配置
- `docker-compose.yml` - 三容器编排配置(db/backend/frontend)
- `.env.example` - 环境变量模板

## 🚀 快速部署(生产环境)

### 1. 准备环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件,修改以下关键配置:
# - SECRET_KEY: 生成随机密钥
# - DB_PASSWORD: 设置数据库密码
# - CORS_ORIGINS: 设置允许的域名
```

### 2. 生成安全密钥
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# 将输出结果填入.env的SECRET_KEY
```

### 3. 启动所有服务
```bash
docker compose up -d
```

### 4. 查看服务状态
```bash
docker compose ps
docker compose logs -f
```

### 5. 初始化数据库
```bash
# 等待服务启动后,执行数据初始化
docker compose exec backend python scripts/init_data.py
docker compose exec backend python scripts/init_courses.py
```

## 🔧 开发环境部署

### 使用SQLite(无需PostgreSQL容器)
```bash
# 只启动后端和前端
docker compose up -d backend frontend

# 或者直接使用本地开发模式(推荐)
cd backend && python main.py  # 8000端口
cd frontend && npm run dev    # 5173端口
```

## 📊 服务架构

```
┌─────────────────────────────────────────┐
│  前端容器 (Nginx)                        │
│  端口: 80                                │
│  - SPA路由支持                           │
│  - API代理到backend:8000                │
│  - Gzip压缩                             │
└───────────┬─────────────────────────────┘
            │
┌───────────▼─────────────────────────────┐
│  后端容器 (FastAPI)                      │
│  端口: 8000                              │
│  - RESTful API                          │
│  - JWT认证                              │
└───────────┬─────────────────────────────┘
            │
┌───────────▼─────────────────────────────┐
│  数据库容器 (PostgreSQL 15)              │
│  端口: 5432                              │
│  - 数据持久化: postgres_data卷           │
└─────────────────────────────────────────┘
```

## 🌐 访问地址

- **前端**: http://localhost (或配置的FRONTEND_PORT)
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 🔍 健康检查

所有服务都配置了健康检查:
```bash
# 查看健康状态
docker compose ps

# 手动检查
curl http://localhost/          # 前端
curl http://localhost:8000/health  # 后端
```

## 🛠️ 常用命令

### 查看日志
```bash
docker compose logs -f           # 所有服务
docker compose logs -f backend   # 仅后端
docker compose logs -f frontend  # 仅前端
```

### 重启服务
```bash
docker compose restart backend   # 重启后端
docker compose restart           # 重启所有
```

### 停止和清理
```bash
docker compose down              # 停止服务
docker compose down -v           # 停止并删除数据卷(注意:会丢失数据)
```

### 重新构建
```bash
docker compose build             # 重新构建镜像
docker compose up -d --build     # 重新构建并启动
```

## ⚠️ 生产环境注意事项

### 必须修改的配置
1. **SECRET_KEY**: 使用强随机密钥
2. **DB_PASSWORD**: 设置强密码
3. **CORS_ORIGINS**: 只允许实际域名
4. **DEBUG**: 设置为false

### 安全建议
- 使用HTTPS(配置SSL证书)
- 定期备份PostgreSQL数据卷
- 定期更新Docker镜像
- 配置防火墙规则
- 监控服务资源使用

### 性能优化
- 调整PostgreSQL配置(`shared_buffers`, `work_mem`等)
- 配置Redis缓存(可选)
- 使用CDN加速静态资源

## 📦 数据备份与恢复

### 备份数据库
```bash
docker compose exec db pg_dump -U smartice training_lms > backup_$(date +%Y%m%d).sql
```

### 恢复数据库
```bash
docker compose exec -T db psql -U smartice training_lms < backup_20251115.sql
```

## 🐛 常见问题

### 1. 端口已被占用
修改`.env`文件中的端口配置:
```bash
BACKEND_PORT=8001
FRONTEND_PORT=8080
```

### 2. 数据库连接失败
检查数据库容器是否健康:
```bash
docker compose logs db
```

### 3. 前端无法访问API
检查nginx.conf中的proxy_pass配置是否正确

## 📚 参考资料

- Docker文档: https://docs.docker.com
- Docker Compose文档: https://docs.docker.com/compose
- PostgreSQL文档: https://www.postgresql.org/docs/15
- Nginx文档: https://nginx.org/en/docs

---

**部署状态**: ✅ 配置文件已就绪,等待Docker Desktop安装后即可部署
**最后更新**: 2025-11-15
