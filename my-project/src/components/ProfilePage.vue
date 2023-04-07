<template>
  <div>
    <div class="container my-4">
      <NavBar />
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <img :src="avatarUrl" class="img-fluid rounded-circle mb-3">
              <div class="mb-2"><b>用户名：</b>{{ username }}</div>
              <div class="mb-2"><b>邮箱：</b>{{ email }}</div>
              <div class="mb-2"><b>性别：</b>{{ gender }}</div>
              <button class="btn btn-primary" @click="logout">退出登录</button>
            </div>
            <div class="col-md-9">
              <h4 class="mb-3">个人介绍</h4>
              <div>{{ bio }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import config from '../config.js'
import router from '../router.js'
import NavBar from "@/components/NavBar.vue";

export default {
  name: 'ProfilePage',
  components: {
    NavBar,
  },
  setup() {
    const avatarUrl = ref('')
    const bio = ref('')
    const email = ref('')
    const gender = ref('')
    const username = ref('')

    const loadProfile = async () => {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${config.apiHost}/users/current`, {
        headers: {
          Authorization: `${token}`
        }
      })
      const profile = response.data
      avatarUrl.value = profile.avatar_url
      bio.value = profile.bio
      email.value = profile.email
      gender.value = profile.gender
      username.value = profile.username
    }

    onMounted(() => {
      loadProfile()
    })

    const logout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      router.push('/login')
    }

    return {
      avatarUrl,
      bio,
      email,
      gender,
      username,
      logout
    }
  }
}
</script>
<style>
.container {
  margin-top: 100px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 30px;
}

@media (max-width: 991.98px) {
  .card-body {
    padding: 20px;
  }
}

.img-fluid {
  width: 100%;
  height: auto;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}

.btn-primary:focus, .btn-primary.focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
}
</style> 