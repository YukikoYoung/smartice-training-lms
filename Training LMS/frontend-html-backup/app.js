const { createApp } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

// Supabase配置（请替换为您的实际配置）
const SUPABASE_URL = 'https://wdpeoyugsxqnpwwtkqsl.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key-here'; // 请替换

// 初始化Supabase客户端
let supabase;
try {
  supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
} catch (error) {
  console.warn('Supabase初始化失败，使用模拟数据模式');
}

// API基础URL
const API_BASE_URL = `${SUPABASE_URL}/functions/v1/lms-api`;

// 创建Vue应用
const app = createApp({
  data() {
    return {
      // 登录状态
      isLoggedIn: false,
      loginLoading: false,
      loginForm: {
        email: '',
        password: ''
      },

      // 当前用户信息
      currentUser: null,

      // 当前视图
      currentView: 'dashboard',

      // 数据看板
      dashboardStats: {
        total_students: 0,
        total_courses: 0,
        completed_courses: 0,
        exam_pass_rate: 0
      },

      // 排行榜
      rankingList: [],

      // 我的课程
      myCourses: [],

      // 课程列表（管理员）
      coursesList: [],

      // 课程对话框
      courseDialogVisible: false,
      courseForm: {
        course_name: '',
        course_type: 'position',
        difficulty: 'basic',
        description: ''
      },

      // 统计数据
      statsTab: 'progress',
      progressStats: [],
      examScores: [],

      // 使用模拟数据
      useMockData: !supabase || SUPABASE_ANON_KEY === 'your-anon-key-here'
    };
  },

  computed: {
    isAdmin() {
      return this.currentUser?.role === 'super_admin' || this.currentUser?.role === 'admin';
    },
    isTrainer() {
      return this.isAdmin || this.currentUser?.role === 'trainer';
    },
    isManager() {
      return this.isTrainer || this.currentUser?.role === 'store_manager';
    }
  },

  mounted() {
    // 检查是否已登录
    const savedUser = localStorage.getItem('lms_current_user');
    if (savedUser) {
      this.currentUser = JSON.parse(savedUser);
      this.isLoggedIn = true;
      this.loadDashboardData();
    }

    // 如果使用模拟数据，显示提示
    if (this.useMockData) {
      ElMessage({
        message: '当前使用演示模式，数据为模拟数据。请配置Supabase后使用真实数据。',
        type: 'warning',
        duration: 5000
      });
    }
  },

  methods: {
    // ========== 登录相关 ==========
    async handleLogin() {
      if (!this.loginForm.email || !this.loginForm.password) {
        ElMessage.error('请输入邮箱和密码');
        return;
      }

      this.loginLoading = true;

      try {
        if (this.useMockData) {
          // 模拟登录
          await this.mockLogin();
        } else {
          // 真实登录
          await this.realLogin();
        }
      } catch (error) {
        ElMessage.error(error.message || '登录失败');
      } finally {
        this.loginLoading = false;
      }
    },

    async mockLogin() {
      // 模拟延迟
      await new Promise(resolve => setTimeout(resolve, 1000));

      // 模拟用户数据
      const mockUsers = {
        'admin@example.com': {
          id: '1',
          email: 'admin@example.com',
          name: '系统管理员',
          role: 'super_admin',
          store: { store_name: '总部' }
        },
        'trainer@example.com': {
          id: '2',
          email: 'trainer@example.com',
          name: '培训负责人',
          role: 'trainer',
          store: { store_name: '总部' }
        },
        'manager@example.com': {
          id: '3',
          email: 'manager@example.com',
          name: '门店经理',
          role: 'store_manager',
          store_id: 1,
          store: { store_name: '望京店' }
        },
        'student@example.com': {
          id: '4',
          email: 'student@example.com',
          name: '张三',
          role: 'student',
          store_id: 1,
          position_id: 1,
          store: { store_name: '望京店' },
          position: { position_name: '服务员' }
        }
      };

      const user = mockUsers[this.loginForm.email];
      if (!user) {
        throw new Error('用户不存在');
      }

      this.currentUser = user;
      this.isLoggedIn = true;
      localStorage.setItem('lms_current_user', JSON.stringify(user));

      ElMessage.success('登录成功！');
      this.loadDashboardData();
    },

    async realLogin() {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: this.loginForm.email,
        password: this.loginForm.password
      });

      if (error) throw error;

      // 获取用户详细信息
      const response = await fetch(`${API_BASE_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${data.session.access_token}`
        }
      });

      const result = await response.json();
      if (!result.success) throw new Error(result.error);

      this.currentUser = result.data;
      this.isLoggedIn = true;
      localStorage.setItem('lms_current_user', JSON.stringify(result.data));
      localStorage.setItem('lms_access_token', data.session.access_token);

      ElMessage.success('登录成功！');
      this.loadDashboardData();
    },

    showDemoAccounts() {
      ElMessageBox.alert(`
        <div style="line-height: 2;">
          <p><strong>超级管理员：</strong></p>
          <p>邮箱: admin@example.com</p>
          <p>密码: 任意密码</p>
          <br>
          <p><strong>培训负责人：</strong></p>
          <p>邮箱: trainer@example.com</p>
          <p>密码: 任意密码</p>
          <br>
          <p><strong>门店经理：</strong></p>
          <p>邮箱: manager@example.com</p>
          <p>密码: 任意密码</p>
          <br>
          <p><strong>普通学员：</strong></p>
          <p>邮箱: student@example.com</p>
          <p>密码: 任意密码</p>
        </div>
      `, '演示账号', {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '知道了'
      });
    },

    handleUserCommand(command) {
      if (command === 'logout') {
        this.handleLogout();
      }
    },

    handleLogout() {
      this.isLoggedIn = false;
      this.currentUser = null;
      localStorage.removeItem('lms_current_user');
      localStorage.removeItem('lms_access_token');
      ElMessage.success('已退出登录');
    },

    getRoleName(role) {
      const roleMap = {
        'super_admin': '超级管理员',
        'admin': '管理员',
        'trainer': '培训负责人',
        'store_manager': '门店管理员',
        'student': '学员'
      };
      return roleMap[role] || role;
    },

    // ========== 菜单切换 ==========
    handleMenuSelect(index) {
      this.currentView = index;
      this.loadViewData(index);
    },

    async loadViewData(view) {
      switch (view) {
        case 'dashboard':
          await this.loadDashboardData();
          break;
        case 'my-courses':
          await this.loadMyCourses();
          break;
        case 'courses':
          await this.loadCoursesList();
          break;
        case 'stats':
          await this.loadStatsData();
          break;
      }
    },

    // ========== 数据加载 ==========
    async loadDashboardData() {
      try {
        if (this.useMockData) {
          this.dashboardStats = {
            total_students: 156,
            total_courses: 24,
            completed_courses: 342,
            exam_pass_rate: 87
          };

          this.rankingList = [
            { user_name: '张三', display_value: '48小时32分钟' },
            { user_name: '李四', display_value: '42小时18分钟' },
            { user_name: '王五', display_value: '38小时45分钟' },
            { user_name: '赵六', display_value: '35小时12分钟' },
            { user_name: '孙七', display_value: '32小时56分钟' }
          ];
        } else {
          const token = localStorage.getItem('lms_access_token');
          const response = await fetch(`${API_BASE_URL}/stats/dashboard`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const result = await response.json();
          if (result.success) {
            this.dashboardStats = result.data;
          }

          await this.loadRanking('study_time');
        }
      } catch (error) {
        console.error('加载数据看板失败:', error);
      }
    },

    async loadRanking(type) {
      try {
        if (this.useMockData) {
          // 已在loadDashboardData中设置
          return;
        }

        const token = localStorage.getItem('lms_access_token');
        const response = await fetch(`${API_BASE_URL}/stats/ranking?type=${type}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const result = await response.json();
        if (result.success) {
          this.rankingList = result.data;
        }
      } catch (error) {
        console.error('加载排行榜失败:', error);
      }
    },

    async loadMyCourses() {
      try {
        if (this.useMockData) {
          this.myCourses = [
            {
              id: 1,
              course_name: '服务员入职培训',
              is_required: true,
              progress: 75,
              completed_contents: 6,
              total_contents: 8
            },
            {
              id: 2,
              course_name: '食品安全与卫生',
              is_required: true,
              progress: 100,
              completed_contents: 5,
              total_contents: 5
            },
            {
              id: 3,
              course_name: '高端接待技巧',
              is_required: false,
              progress: 30,
              completed_contents: 3,
              total_contents: 10
            },
            {
              id: 4,
              course_name: '红酒知识入门',
              is_required: false,
              progress: 0,
              completed_contents: 0,
              total_contents: 6
            }
          ];
        } else {
          const token = localStorage.getItem('lms_access_token');
          const response = await fetch(`${API_BASE_URL}/learning/my-courses`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const result = await response.json();
          if (result.success) {
            this.myCourses = result.data;
          }
        }
      } catch (error) {
        console.error('加载我的课程失败:', error);
      }
    },

    async loadCoursesList() {
      try {
        if (this.useMockData) {
          this.coursesList = [
            {
              id: 1,
              course_name: '服务员入职培训',
              course_type: 'position',
              difficulty: 'basic',
              status: 'PUBLISHED'
            },
            {
              id: 2,
              course_name: '食品安全与卫生',
              course_type: 'general',
              difficulty: 'basic',
              status: 'PUBLISHED'
            },
            {
              id: 3,
              course_name: '高端接待技巧',
              course_type: 'position',
              difficulty: 'intermediate',
              status: 'PUBLISHED'
            },
            {
              id: 4,
              course_name: '新菜品培训（待发布）',
              course_type: 'special',
              difficulty: 'basic',
              status: 'DRAFT'
            }
          ];
        } else {
          const token = localStorage.getItem('lms_access_token');
          const response = await fetch(`${API_BASE_URL}/courses`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const result = await response.json();
          if (result.success) {
            this.coursesList = result.data;
          }
        }
      } catch (error) {
        console.error('加载课程列表失败:', error);
      }
    },

    async loadStatsData() {
      try {
        if (this.useMockData) {
          this.progressStats = [
            { user_name: '张三', total_courses: 8, completed_courses: 6, progress_rate: 75 },
            { user_name: '李四', total_courses: 6, completed_courses: 6, progress_rate: 100 },
            { user_name: '王五', total_courses: 10, completed_courses: 7, progress_rate: 70 },
            { user_name: '赵六', total_courses: 5, completed_courses: 3, progress_rate: 60 }
          ];

          this.examScores = [
            {
              user: { name: '张三' },
              exam: { exam_name: '服务员结业考试' },
              score: 92,
              is_passed: true,
              submit_time: '2025-11-10 14:30:00'
            },
            {
              user: { name: '李四' },
              exam: { exam_name: '食品安全考试' },
              score: 88,
              is_passed: true,
              submit_time: '2025-11-09 10:15:00'
            },
            {
              user: { name: '王五' },
              exam: { exam_name: '服务员结业考试' },
              score: 55,
              is_passed: false,
              submit_time: '2025-11-08 16:45:00'
            }
          ];
        } else {
          const token = localStorage.getItem('lms_access_token');

          // 加载学习进度统计
          const progressResponse = await fetch(`${API_BASE_URL}/stats/learning-progress`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const progressResult = await progressResponse.json();
          if (progressResult.success) {
            this.progressStats = progressResult.data;
          }

          // 加载考试成绩统计
          const scoresResponse = await fetch(`${API_BASE_URL}/stats/exam-scores`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const scoresResult = await scoresResponse.json();
          if (scoresResult.success) {
            this.examScores = scoresResult.data;
          }
        }
      } catch (error) {
        console.error('加载统计数据失败:', error);
      }
    },

    // ========== 课程管理 ==========
    openCourseDialog() {
      this.courseForm = {
        course_name: '',
        course_type: 'position',
        difficulty: 'basic',
        description: ''
      };
      this.courseDialogVisible = true;
    },

    async saveCourse() {
      if (!this.courseForm.course_name) {
        ElMessage.error('请输入课程名称');
        return;
      }

      try {
        if (this.useMockData) {
          await new Promise(resolve => setTimeout(resolve, 500));
          ElMessage.success('课程创建成功（模拟）');
          this.courseDialogVisible = false;
          this.loadCoursesList();
        } else {
          const token = localStorage.getItem('lms_access_token');
          const response = await fetch(`${API_BASE_URL}/courses`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.courseForm)
          });

          const result = await response.json();
          if (result.success) {
            ElMessage.success('课程创建成功');
            this.courseDialogVisible = false;
            this.loadCoursesList();
          } else {
            throw new Error(result.error);
          }
        }
      } catch (error) {
        ElMessage.error('创建课程失败: ' + error.message);
      }
    },

    editCourse(course) {
      ElMessage.info('编辑功能开发中...');
    },

    async deleteCourse(course) {
      try {
        await ElMessageBox.confirm('确定要删除该课程吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });

        if (this.useMockData) {
          await new Promise(resolve => setTimeout(resolve, 500));
          ElMessage.success('课程删除成功（模拟）');
          this.loadCoursesList();
        } else {
          const token = localStorage.getItem('lms_access_token');
          const response = await fetch(`${API_BASE_URL}/courses/${course.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          const result = await response.json();
          if (result.success) {
            ElMessage.success('课程删除成功');
            this.loadCoursesList();
          } else {
            throw new Error(result.error);
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除课程失败: ' + error.message);
        }
      }
    },

    openCourse(course) {
      ElMessage.info('课程学习界面开发中...');
    }
  }
});

// 注册Element Plus Icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 使用Element Plus
app.use(ElementPlus);

// 挂载应用
app.mount('#app');
