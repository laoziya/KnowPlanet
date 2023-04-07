<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">首页</router-link>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <div class="navbar-nav ms-auto" style="flex-direction: row">
          <div class="nav-item">
            <router-link
              to="/createc"
              class="nav-link"
              :class="{ active: currentRoute === '/createc' }"
              style="display: inline-block; color: black; text-decoration: none"
              >新建课程</router-link
            >
          </div>
          <div class="nav-item">
            <router-link
              to="/courses"
              class="nav-link"
              :class="{ active: currentRoute === '/courses' }"
              style="display: inline-block; color: black; text-decoration: none"
              >我的课程</router-link
            >
          </div>
          <div class="nav-item">
            <router-link
              to="/about"
              class="nav-link"
              :class="{ active: currentRoute === '/about' }"
              style="display: inline-block; color: black; text-decoration: none"
              >关于我们</router-link
            >
          </div>
          <div v-if="isAuthenticated" class="nav-item dropdown">
            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <router-link to="/profile" class="dropdown-item">个人信息</router-link>
              <div class="dropdown-divider"></div>
            </div>
          </div>
          <div v-else class="nav-item">
            <router-link
              to="/login"
              class="nav-link"
              :class="{ active: currentRoute === '/login' }"
              style="display: inline-block; color: black; text-decoration: none"
              >登录</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    currentRoute: {
      type: String,
      required: true,
    },
  },
  computed: {
    isAuthenticated() {
      return localStorage.getItem("isAuthenticated") === "true";
    },
    currentUser() {
      return JSON.parse(localStorage.getItem("currentUser"));
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("isAuthenticated");
      localStorage.removeItem("currentUser");
      location.reload();
    },
  },
};
</script>

<style>
nav {
  background-color: #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
}

.container-fluid {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

nav a {
  display: block;
  text-decoration: none;
  color: black;
  padding: 10px;
}

nav a:hover {
  background-color: #dcdcdc;
}

.navbar-collapse {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.navbar-nav {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}

.dropdown-menu {
  background-color: #f0f0f0;
  border: none;
  border-radius: 0;
  margin-top: 0;
  display: inline-block;
}

.dropdown-item {
  color: black;
  text-decoration: none;
}

.dropdown-item:hover {
  background-color: #dcdcdc;
}

.navbar-brand {
  color: black;
  text-decoration: none;
  font-weight: bold;
  font-size: 20px;
  padding: 10px;
}

.active {
  background-color: #dcdcdc;
}

@media (max-width: 767px) {
  .navbar-nav {
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
  }
}
</style>
