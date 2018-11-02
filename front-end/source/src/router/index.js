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
				name: 'finance-analysis',
				meta: {
				  title: '财务分析',
				  hideInMenu: true
				},
				component: () => import('@/components/finance-analysis')
			},
			{
				path: '/cash_flow',
				name: 'cash-flow',
				meta: {
				  title: '财务分析',
				  hideInMenu: true
				},
				component: () => import('@/components/cash-flow')
			},
			{
				path: '/fellow/list',
				name: 'fellow-list',
				meta: {
				  title: '会员列表',
				  hideInMenu: true
				},
				component: () => import('@/components/fellows/fellow-list/')
			},
			{
				path: '/fellow/consumptions',
				name: 'fellow-consumption',
				meta: {
				  title: '会员消费记录',
				  hideInMenu: true
				},
				component: () => import('@/components/fellows/fellow-consumptions/')
			},
			{
				path: '/employee/list',
				name: 'employee-list',
				meta: {
				  title: '员工列表',
				  hideInMenu: true
				},
				component: () => import('@/components/employees/employee-list/')
			},
			{
				path: '/employee/salary_record',
				name: 'salary_record',
				meta: {
				  title: '员工列表',
				  hideInMenu: true
				},
				component: () => import('@/components/employees/employee-money/')
			},
			{
				path: '/setting/employee_type',
				name: 'employee-type-setting',
				meta: {
				  title: '人员类别管理',
				  hideInMenu: true
				},
				component: () => import('@/components/setting/employee-type/')
			},
			{
				path: '/setting/fellow_type',
				name: 'fellow-type-setting',
				meta: {
				  title: '会员卡类型管理',
				  hideInMenu: true
				},
				component: () => import('@/components/setting/fellow-type/')
			},
			{
				path: '/setting/users',
				name: 'user-access-manage',
				meta: {
				  title: '登陆权限管理',
				  hideInMenu: true
				},
				component: () => import('@/components/setting/user-access/')
			}
		]
	}
  ]
})
