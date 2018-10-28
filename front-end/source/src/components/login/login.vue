<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/login-form'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
  name: "Login",
  components: {
    LoginForm
  },
  data () {
    return {
    }
  },
  created: function(){
    if (localStorage.activeMenuName)
      delete localStorage.activeMenuName
  },
  methods: {
    handleSubmit ({ userName, password }) {
      this.$http.post(baseAPIUrl + "login",{
          "username": userName, 
          "password": password
      }).then(response => {
          this.$Message.success('登陆成功，欢迎' + userName);
          this.$router.push({
            name: "dashboard"
          });
        }, response => {
          const config = {
            title: "登陆失败",
            content: "请确认账号密码",
            width: "300px"
          };
          this.$Modal.error(config);
      });
    }
  }
}
</script>
