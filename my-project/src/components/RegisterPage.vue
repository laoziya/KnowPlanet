<template>
  <div class="container">
    <h1 class="title">Create your account</h1>
    <form class="form" @submit.prevent="register">
      <div class="form-group">
        <label for="username" class="form-label">Username</label>
        <input type="text" id="username" v-model="username" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input type="email" id="email" v-model="email" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" required>
      </div>
      <div class="form-group">
        <label for="confirm-password" class="form-label">Confirm Password</label>
        <input type="password" id="confirm-password" v-model="confirmPassword" class="form-control" required>
        <p v-if="password && password !== confirmPassword" class="error">Passwords do not match.</p>
      </div>
      <button type="submit" class="btn btn-primary">Sign up for KnowPlanet</button>
    </form>
    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    <div class=“login-link”>
<p>Already have an account? <router-link to="/login">Log in</router-link></p>
</div>
  </div>
</template>
<script>
import axios from 'axios';
import config from '../config.js'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      errorMessage: '',
    };
  },
  methods: {
    register() {
      if (this.password !== this.confirmPassword) {
        return;
      }

      axios.post(config.apiHost+'/users/', {
        username: this.username,
        email: this.email,
        password: this.password,
      })
        .then(() => {
          // 注册成功后的操作
          //this.$router.push('/login');
            this.errorMessage = 'Registration successful. Redirecting to login page in 3 seconds.';
            setTimeout(() => {
              this.$router.push('/login');
            }, 3000);
        })
        .catch(error => {
          // 注册失败后的操作
          this.errorMessage = error.response.data.message;
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

: pointer {
background-color: #2ea44f;
color: #fff;
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