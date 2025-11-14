#!/bin/bash

echo "=================================="
echo "SmartIce培训系统 - 启动脚本"
echo "=================================="

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python 3.8+"
    exit 1
fi

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  未检测到虚拟环境，建议使用虚拟环境"
    echo "创建虚拟环境: python3 -m venv venv"
    echo "激活虚拟环境: source venv/bin/activate"
    echo ""
    read -p "是否继续运行？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查依赖是否安装
echo "[1/4] 检查依赖..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "  依赖未安装，正在安装..."
    pip3 install -r requirements.txt
else
    echo "  ✓ 依赖已安装"
fi

# 检查.env文件
echo "[2/4] 检查配置..."
if [ ! -f .env ]; then
    echo "  ❌ .env文件不存在"
    exit 1
fi
echo "  ✓ 配置文件存在"

# 检查数据库是否存在
echo "[3/4] 检查数据库..."
if [ ! -f training_lms.db ]; then
    echo "  数据库不存在，将在首次启动时自动创建"
fi

# 启动服务
echo "[4/4] 启动服务..."
echo ""
echo "=================================="
echo "后端服务启动中..."
echo "访问地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "前端测试: 使用Live Server打开 ../frontend-test/index.html"
echo "=================================="
echo ""

python3 main.py
