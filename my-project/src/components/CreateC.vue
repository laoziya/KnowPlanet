<template>
  <div>
    <h1>Create Course</h1>
    <form @submit.prevent="createCourse">
      <div>
        <label for="title">Title</label>
        <input type="text" id="title" v-model="title">
      </div>
      <div>
        <label for="description">Description</label>
        <textarea id="description" v-model="description"></textarea>
      </div>
      <div>
        <button type="submit">Create Course</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import config from '../config.js'

export default {
  data() {
    return {
      title: '',
      description: '',
    }
  },
  methods: {
  createCourse() {
    const token = localStorage.getItem('token')
    axios.post(config.apiHost + '/courses/', {
      title: this.title,
      description: this.description,
    }, {
      headers: {
        Authorization: `${token}`,
        'Access-Control-Allow-Origin': '*'
      },
    }).then(response => {
      // 课程创建成功，跳转到新创建的课程详情页面
      this.$router.push({ name: 'coursedetail', params: { id: response.data.id } });
    }).catch(error => {
      console.error(error);
    });
  }
}
}
</script>
