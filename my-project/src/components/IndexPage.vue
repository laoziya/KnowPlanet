<template>
  <div class="container">
    <NavBar />
    <div class="search-box-container">
      <div class="search-box">
        <input type="text" placeholder="搜索课程" />
        <i class="fa fa-search"></i>
      </div>
    </div>
    <div class="course-grid">
      <div v-for="course in courses" :key="course.id" class="course-card" @click="goToCourseDetail(course.id)">
        <img :src="course.image || defaultImage" alt="course cover" />
        <h3 class="course-title">{{ course.title }}</h3>
        <p class="course-description">{{ course.description }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import config from "@/config";

export default {
  name: "IndexPage",
  components: {
    NavBar,
  },
  data() {
    return {
      courses: [],
      defaultImage: "https://via.placeholder.com/150",
    };
  },
  mounted() {
    this.fetchCourses();
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await fetch(config.apiHost + "/courses/");
        const data = await response.json();
        this.courses = data;
      } catch (error) {
        console.error(error);
      }
    },
    goToCourseDetail(courseId) {
      this.$router.push({ name: "coursedetail", params: { id: courseId } });
    },
  },
};
</script>
<style>
  .search-box-container {
    display: flex;
    justify-content: center;
    margin-top: 50px;
  }

  .search-box {
    display: flex;
    align-items: center;
    width: 400px;
    height: 40px;
    border-radius: 20px;
    border: 1px solid #ccc;
    transition: border-color 0.3s ease-in-out;
  }

  .search-box input {
    width: 90%;
    height: 95%;
    border: none;
    outline: none;
    font-size: 16px;
    margin: 15px
  }

  .search-box i {
    font-size: 20px;
    margin: 0 10px;
    color: #ccc;
  }

  .search-box input:focus {
    border-color: #3a8ee6;
  }

  .course-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 20px;
    margin-top: 80px;
    width: 80%
  }

  .course-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px #ccc;
  }

  .course-card img {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 10px;
  }

  .course-title {
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
  }

  .course-description {
    font-size: 14px;
    color: #999;
    margin-top: 10px;
    text-align: center;
  }

  .default-cover {
    width: 100%;
    height: 150px;
    background-color: #ccc;
    border-radius: 10px;
  }
</style>
