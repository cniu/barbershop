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
		  title: '首页',
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
				  notCache: true
			},
			component: () => import('@/components/dashboard')
			},
			{
				path: '/sell_items',
				name: 'sell-items',
				meta: {
				  hideInMenu: true,
				  title: '开单记录',
				  notCache: true
			},
			component: () => import('@/components/sell-items')
			},
			{
				path: '/finance_analysis',
				name: 'finance_analysis',
				meta: {
				  title: '财务分析',
				  hideInMenu: true
				},
				component: () => import('@/components/finance-analysis')
			},
			{
				path: '/account/list',
				name: 'account-list',
				meta: {
				  title: '会员列表',
				  hideInMenu: true
				},
				component: () => import('@/components/account/account-list/')
			},
			{
				path: '/account/consumptions',
				name: 'account-consumption',
				meta: {
				  title: '会员消费记录',
				  hideInMenu: true
				},
				component: () => import('@/components/account/account-consumptions/')
			}
		]
	}
  ]
})
