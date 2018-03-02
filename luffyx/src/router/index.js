import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Course from '@/components/Course'
import DegreeCourse from '@/components/DegreeCourse'
import DegreeCourseDetail from '@/components/DegreeCourseDetail'
import CourseDetail from '@/components/CourseDetail'
import Login from '@/components/Login'
import News from '@/components/News'
import NewsDetail from '@/components/NewsDetail'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/course',
      name: 'course',
      component: Course
    },
    {
      path: '/course-detail/:id/',
      name: 'course-detail',
      component: CourseDetail
    },
    {
      path: '/degreecourse',
      name: 'degreeCourse',
      component: DegreeCourse
    },
    {
      path: '/degreecourse-detail/:id',
      name: 'degreeourseDetail',
      component: DegreeCourseDetail
    },
     {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/index',
      name: 'index',
      component: Index
    },
    {
      path: '/news',
      name: 'news',
      component: News
    },
    {
      path: '/newsDetail/:id/',
      name: 'newsDetail',
      component: NewsDetail
    },
  ],
  mode: 'history'
})
