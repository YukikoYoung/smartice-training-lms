#!/bin/bash
# API端点集成测试脚本

BASE_URL="http://localhost:8000"
PASSED=0
FAILED=0
TOTAL=0

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=$3
    local description=$4
    local headers=$5

    TOTAL=$((TOTAL + 1))

    if [ -z "$headers" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "${BASE_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "${BASE_URL}${endpoint}" -H "$headers")
    fi

    status_code=$(echo "$response" | tail -n 1)

    if [ "$status_code" -eq "$expected_status" ]; then
        print_success "$method $endpoint - $description"
        PASSED=$((PASSED + 1))
        return 0
    else
        print_error "$method $endpoint - 状态码: $status_code (期望: $expected_status)"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo ""
echo "============================================================"
echo "  SmartIce LMS - API端点集成测试"
echo "============================================================"
echo ""

# 1. 登录获取token
print_info "正在登录..."
login_response=$(curl -s -X POST "${BASE_URL}/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo $login_response | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    print_error "登录失败，无法获取token"
    exit 1
fi

username=$(echo $login_response | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['full_name'])" 2>/dev/null)
print_success "登录成功 - 用户: $username"
echo ""

print_info "开始测试API端点..."
echo ""

# 测试端点
test_endpoint "GET" "/health" 200 "健康检查" ""
test_endpoint "GET" "/" 200 "根路径" ""
test_endpoint "GET" "/api/auth/me" 200 "获取当前用户信息" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/courses/" 200 "获取课程列表" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/courses/1" 200 "获取课程详情" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/courses/1/chapters" 200 "获取课程章节列表" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/exams/" 200 "获取考试列表" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/exams/1" 200 "获取考试详情" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/learning/courses/progress" 200 "获取课程学习进度" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/learning/chapters/progress" 200 "获取章节学习进度" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/learning/stats" 200 "获取学习统计" "Authorization: Bearer $TOKEN"
test_endpoint "GET" "/api/users/" 200 "获取用户列表" "Authorization: Bearer $TOKEN"

# 打印汇总
echo ""
echo "============================================================"
echo "  测试结果汇总"
echo "============================================================"
echo "总计: $TOTAL 个测试"
echo -e "${GREEN}通过: $PASSED 个${NC}"
echo -e "${RED}失败: $FAILED 个${NC}"

success_rate=$(echo "scale=1; $PASSED * 100 / $TOTAL" | bc)
echo "成功率: ${success_rate}%"
echo "============================================================"
echo ""

if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi
