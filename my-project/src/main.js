import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import LessonDetail from './components/LessonDetail'
import CourseDiscussion from './components/CourseDiscussion'


import axios from 'axios';

// 全局导航守卫
router.beforeEach(async (to, from, next) => {
  // 如果要前往的页面不是登录页或注册页
  if (to.path !== '/login' && to.path !== '/register') {
    try {
      // 发送请求验证用户登录状态
      const response = await axios.get('http://192.168.220.110:9000/api/v1/users/check', {
        headers: { Authorization: localStorage.getItem('token') },
      });
      if (response.status === 200) {
        // 已登录，放行
        next();
      } else {
        // 未登录，重定向到登录页
        next('/login');
      }
    } catch (error) {
      // 发生错误，重定向到登录页
      next('/login');
    }
  } else {
    // 如果要前往的页面是登录页或注册页
    // 判断用户是否已经登录
    const token = localStorage.getItem('token');
    if (token) {
      // 已登录，重定向到主页
      next('/');
    } else {
      // 未登录，放行
      next();
    }
  }
});


const app = createApp(App).use(router)
app.component('LessonDetail', LessonDetail)
app.component('CourseDiscussion', CourseDiscussion)
app.mount('#app')


