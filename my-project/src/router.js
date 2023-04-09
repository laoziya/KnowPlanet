import Register from './components/RegisterPage'
import Login from './components/LoginPage'
import IndexPage from './components/IndexPage'
import NavBar from './components/NavBar'
import Profile from './components/ProfilePage'
import CourseDetail from './components/CourseDetail'
import LessonEdit from './components/LessonEdit'
import CreateC from './components/CreateC'
import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'index',
    component: IndexPage

  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/navbar',
    name: 'navbar',
    component: NavBar
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile
  },
  {
    path: '/course/:id',
    name: 'coursedetail',
    component: CourseDetail
  },
  {
    path: '/lesson/:lesson_id/edit',
    name: 'lessonedit',
    component: LessonEdit
  },
  {
    path: '/createc',
    name: 'createc',
    component: CreateC
  },
]
  

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router
