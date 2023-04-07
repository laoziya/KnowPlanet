<template>
  <div class="container">
    <h1 class="title">Login</h1>
    <form class="form" @submit.prevent="login">
      <div class="form-group">
        <label class="form-label" for="username_or_email">Username or Email:</label>
        <input class="form-control" type="text" id="username_or_email" v-model="username_or_email">
      </div>
      <div class="form-group">
        <label class="form-label" for="password">Password:</label>
        <input class="form-control" type="password" id="password" v-model="password">
      </div>
      <button class="btn" type="submit">Login</button>
    </form>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div class=“login-link”>
<p>没有账号? <router-link to="/register">注册</router-link></p>
</div>
  </div>
</template>
<script>
import axios from 'axios';
import config from '../config.js'

export default {
  data() {
    return {
      username_or_email: '',
      password: '',
      error: null,
    };
  },
  methods: {
    login() {

      axios.post(config.apiHost + '/users/login', {
        username_or_email: this.username_or_email,
        password: this.password,
      })
        .then(response => {
          // 登录成功后的操作
          console.log(response.data);
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('isAuthenticated', 'true'); // 设置本地存储变量
          this.$router.push('/');
        })
        .catch(error => {
          // 登录失败后的操作
          this.error = error.response.data.message;
        });
    },
  },
};
</script>
<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  margin-top: 3rem;
  margin-bottom: 2rem;
}

.form {
  width: 30rem;
  margin-bottom: 3rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  cursor: pointer;
  color: #fff;
  background-color: #28a745;
}

.btn:hover {
  background-color: #2c974b;
}

.btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.5);
  outline: none;
}

.error-message {
  color: #cb2431;
  font-weight: bold;
  margin-top: 1rem;
}

.error {
  color: #cb2431;
  margin-top: 0.5rem;
  font-weight: bold;
}
</style>