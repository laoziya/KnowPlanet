<template>
  <div class="lesson-detail">
    <div class="lesson-header">
      <h1>{{ lessonName }}</h1>
    </div>
    <div class="lesson-content">
      <div v-html="lessonContent"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import config from "@/config";
export default {
  props: {
    lessonId: {
      type: Number,
      required: true,
    },
  },
  name: "LessonDetail",
  data() {
    return {
      lessonName: "",
      lessonContent: "",
    };
  },
  watch: {
    lessonId(newVal) {
      this.getLessonDetail(newVal);
    },
  },
  mounted() {
    this.getLessonDetail();
  },
  methods: {
    async getLessonDetail() {
      try {
        const response = await axios.get(`${config.apiHost}/lessons/${this.lessonId}`);
        this.lessonName = response.data.name;
        this.lessonContent = response.data.content;
        console.log('lessonId'+this.lessonId)
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.lesson-header h1 {
  font-size: 24px;
  font-weight: bold;
}

.lesson-content {
  font-size: 16px;
  line-height: 1.8;
}
</style>
