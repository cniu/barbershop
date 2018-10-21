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
const headers = {
    'Content-Type': 'application/json;charset=utf-8'
  };
export default {
  name: "Login",
  components: {
    LoginForm
  },
  methods: {
    handleSubmit ({ userName, password }) {
      this.$http.post(baseAPIUrl + "login",{
          "username": userName, 
          "password": password
      }, {headers: headers}).then(function(data, status){
        console.log(data);
        this.$router.push({
          name: "home"
        })
      });
      // this.handleLogin({ userName, password }).then(res => {
      //   this.getUserInfo().then(res => {
      //     this.$router.push({
      //       name: this.$config.homeName
      //     })
      //   })
      // })
    }
  }
}
</script>
