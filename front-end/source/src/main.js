// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import config from '../config'
import '@/assets/icons/iconfont.css'

import 'iview/dist/styles/iview.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import VueResource from 'vue-resource';
import iView from 'iview'
import BootstrapVue from 'bootstrap-vue'

Vue.config.productionTip = false

Vue.use(iView)
Vue.use(VueResource);
Vue.use(BootstrapVue);

/**
 * @description 全局注册应用配置
 */
Vue.prototype.$config = config

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})