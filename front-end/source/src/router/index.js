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
		component: () => import('@/components/login/login.vue')
	},
	{
		path: '/home_single',
		name: 'home_single',
		meta: {
		  title: 'Home',
		  hideInMenu: true
		},
		component: () => import('@/components/home.vue')
	},
	// {
	// 	path: '/',
	// 	name: '_home',
	// 	redirect: '/home',
	// 	component: Main,
	// 	meta: {
	// 	  hideInMenu: true,
	// 	  notCache: true
	// 	},
	// 	children: [
	// 	  {
	// 	    path: '/home',
	// 	    name: 'home',
	// 	    meta: {
	// 	      hideInMenu: true,
	// 	      title: '首页',
	// 	      notCache: true,
	// 	      icon: 'md-home'
	// 	    },
	// 	    component: () => import('@/components/home.vue')
	// 	  }
	// 	]
	// }
  ]
})
