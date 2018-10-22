import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/admin-main'

Vue.use(Router)

export default new Router({
  routes: [
	{
		path: '/login',
		name: 'login',
		meta: {
		  title: 'Login - 登录',
		  hideInMenu: true
		},
		component: () => import('@/components/login')
	},
	{
		path: '/index',
		name: 'index',
		meta: {
		  title: '功能首页',
		  hideInMenu: true
		},
		component: () => import('@/components/index')
	},
	{
		path: '/',
		name: '_home',
		redirect: '/dashboard',
		component: Main,
		meta: {
		  hideInMenu: true,
		  notCache: true
		},
		children: [
		  {
		    path: '/dashboard',
		    name: 'dashboard',
		    meta: {
		      hideInMenu: true,
		      title: '管理页面',
		      notCache: true,
		      icon: 'md-home'
		    },
		    component: () => import('@/components/dashboard')
		  }
		]
	}
  ]
})
