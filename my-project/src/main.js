import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import LessonDetail from './components/LessonDetail'


// 全局导航守卫
router.beforeEach((to, from, next) => {
    // 如果要前往的页面不是登录页或注册页
    if (to.path !== '/login' && to.path !== '/register') {
      // 判断用户是否已经登录
      const isAuthenticated = localStorage.getItem('isAuthenticated');
      if (isAuthenticated === 'true') {
        // 已登录，放行
        next();
      } else {
        // 未登录，重定向到登录页
        next('/login');
      }
    } else {
      // 如果要前往的页面是登录页或注册页
      // 判断用户是否已经登录
      const isAuthenticated = localStorage.getItem('isAuthenticated');
      if (isAuthenticated === 'true') {
        // 已登录，重定向到主页
        next('/');
      } else {
        // 未登录，放行
        next();
      }
    }
  });

const app=createApp(App).use(router)
app.component('LessonDetail', LessonDetail)
app.mount('#app')


