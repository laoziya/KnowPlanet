<template>
  <div class="container">
    <div class="sidebar" :class="{ collapsed: collapsed }">
      <div class="sidebar-header">
        <h2>{{ course.title }}</h2>
      </div>
      <ul class="sidebar-nav">
        <li>
          <a class="link" @click="addLesson">
            <span>添加课时</span>
          </a>
        </li>
        <li>
          <router-link :to="{ name: 'coursedetail', params: { id: course.id } }"
          @click="goIndex()"
          >
            <i class="fa-home"></i>
            <div class="name"><span>课程主页</span></div>
          </router-link>
        </li>

        <li
          v-for="lesson in lessons"
          :key="lesson.id"
          @click="selectedLesson = lesson.id"
          :class="{ selected: selectedLesson === lesson.id }"
          :data-id="lesson.id"
        >
          <a class="link" @click="goToLessonDetail(course.id, lesson.id)">
            <i class="fas"></i>
            <div class="name lesson-name">
              <span>{{ lesson.name }}</span>
            </div>
            <div class="lesson-actions">
              <router-link
                class="btn btn-edit"
                :to="{ name: 'lessonedit', params: { lesson_id: lesson.id } }"
              >
                <i class="edit"></i>
              </router-link>
              <button class="btn btn-delete" @click.stop="deleteLesson(lesson)">
                <i class="del"></i>
              </button>
            </div>
          </a>
        </li>
      </ul>
    </div>
    <div class="main-content">
    <div class="lessondetail-container" v-if="showLesson">
      <LessonDetail :lessonId="currentLessonId"></LessonDetail>
    </div>

      <div class="content-header" v-if="showIndex">
        <h1>{{ course.title }}</h1>
        <p>{{ course.description }}</p>
      </div>
      <div class="discussion-container" v-if="showIndex">
        <div class="labels-container">
          <h3>标签</h3>
          <div class="labels-list">
            <span class="label">HTML</span>
            <span class="label">CSS</span>
            <span class="label">JavaScript</span>
          </div>
        </div>
        <div class="topics-container">
          <h3>话题</h3>
          <div class="topics-list">
            <div class="topic">
              <div class="topic-header">
                <span class="topic-title">如何实现一个简单的Vue组件？</span>
                <div class="topic-meta">
                  <span class="topic-author">张三</span>
                  <span class="topic-time">3分钟前</span>
                </div>
              </div>
              <div class="topic-content">
                <p>
                  我想要实现一个简单的Vue组件，但是不知道从哪里开始，请各位大佬指点迷津！
                </p>
              </div>
              <div class="topic-actions">
                <button class="btn btn-reply">
                  <i class="fas fa-reply"></i>
                  <span>回复</span>
                </button>
              </div>
            </div>
            <div class="topic">
              <div class="topic-header">
                <span class="topic-title">如何用CSS实现一个圆形按钮？</span>
                <div class="topic-meta">
                  <span class="topic-author">李四</span>
                  <span class="topic-time">1小时</span>
                  <span class="tag">CSS</span>
                  <span class="tag">前端</span>
                  <span class="tag">圆形按钮</span>
                </div>
                <div class="topic-content">
                  <p>我想实现一个圆形按钮，应该怎么做？</p>
                </div>
              </div>
              <div class="topic">
                <div class="topic-header">
                  <span class="topic-title">Vue组件间的通信方式有哪些？</span>
                  <span class="tag">Vue</span>
                  <span class="tag">前端</span>
                  <span class="tag">组件通信</span>
                </div>
                <div class="topic-content">
                  <p>我想知道Vue组件间通信的方式，求大佬解答！</p>
                </div>
              </div>
            </div>
            <div class="tags">
              <h3>标签</h3>
              <div class="tag-list">
                <span class="tag">HTML</span>
                <span class="tag">CSS</span>
                <span class="tag">JavaScript</span>
                <span class="tag">Vue</span>
                <span class="tag">React</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <h2>添加课时</h2>
        <form @submit.prevent="submitLesson">
          <div class="form-group">
            <label for="lessonName">课时名称：</label>
            <input type="text" id="lessonName" v-model="lessonName" />
          </div>
          <button type="submit">添加</button>
          <button type="button" @click="closeModal">取消</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import config from "@/config";
import LessonDetail from '@/components/LessonDetail';

export default {
  name: "CourseDetail",
  data() {
    return {
      course: {},
      lessons: [],
      selectedLesson: "",
      LessonDetail,
      tags: [],
      topics: [],
      newTag: "",
      newTopic: "",
      currentLessonId: null,
      showLesson: false,
      showIndex: true,
    };
  },
  async created() {
    await this.fetchCourse();
    await this.fetchLessons();
    await this.fetchTags();
    await this.fetchTopics();
  },
  methods: {
    async fetchCourse() {
      try {
        const response = await axios.get(
          `${config.apiHost}/courses/${this.$route.params.id}`
        );
        this.course = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchLessons() {
      try {
        const response = await axios.get(
          `${config.apiHost}/courses/${this.$route.params.id}/lessons`
        );
        this.lessons = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchTags() {
      try {
        const response = await axios.get(
          `${config.apiHost}/courses/${this.$route.params.id}/tags`
        );
        this.tags = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchTopics() {
      try {
        const response = await axios.get(
          `${config.apiHost}/courses/${this.$route.params.id}/topics`
        );
        this.topics = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    //添加课时
    async addLesson() {
      const name = prompt("请输入课时名称");
      if (name) {
        const data = {
          course_id: this.course.id,
          name: name,
        };
        try {
          const token = localStorage.getItem("token");
          await axios.post(config.apiHost + "/lessons/", data, {
            headers: {
              Authorization: `${token}`,
            },
          });
          this.fetchLessons();
        } catch (error) {
          console.error(error);
        }
      }
    },
    async deleteLesson(lesson) {
      try {
        await axios.delete(`${config.apiHost}/lessons/${lesson.id}`);
        this.lessons = this.lessons.filter((l) => l.id !== lesson.id);
      } catch (error) {
        console.error(error);
      }
    },
    async addTag() {
      try {
        const response = await axios.post(`${config.apiHost}/tags`, {
          name: this.newTag,
        });
        const newTag = response.data;
        this.tags.push(newTag);
        this.newTag = "";
      } catch (error) {
        console.error(error);
      }
    },
    async addTopic() {
      try {
        const response = await axios.post(`${config.apiHost}/topics`, {
          title: this.newTopic,
        });
        const newTopic = response.data;
        this.topics.push(newTopic);
        this.newTopic = "";
      } catch (error) {
        console.error(error);
      }
    },
    goToLessonDetail(course_id, lesson_id) {
      this.currentLessonId = lesson_id;
      this.showLesson = true;
      this.showIndex = false;
      console.log(this.showLesson)
      console.log(this.currentLessonId)
      // this.$router.push({ name: 'lessondetail', params: { course_id: course_id, lesson_id: lesson_id } })
    },
    goIndex() {
      this.showLesson = false;
      this.showIndex = true;
      
    },
  },
  mounted() {
    // 获取所有会话元素和按钮元素
    const items = document.querySelectorAll(".sidebar-nav li");
    const buttons = document.querySelectorAll(".sidebar-nav li button");
    console.log('xxx:'+this.$options.components);
    // 遍历所有会话元素
    items.forEach((item) => {
      // 监听鼠标点击事件
      item.addEventListener("click", (event) => {
        // 阻止默认行为
        event.preventDefault();
        // 遍历所有按钮元素
        buttons.forEach((button) => {
          // 如果是当前点击的会话对应的按钮，则设置为可见状态
          if (button.dataset.lessonId === event.currentTarget.dataset.lessonId) {
            button.style.display = "flex";
            // 否则，设置为隐藏状态
          } else {
            button.style.display = "none";
          }
        });
      });
    });

    
  },
  watch: {
    // 监听课时列表数据的变化
    lessons: {
      handler() {
        // 重新获取所有会话元素和按钮元素
        const items = document.querySelectorAll(".sidebar-nav li");
        const buttons = document.querySelectorAll(".sidebar-nav li button");

        // 遍历所有会话元素
        items.forEach((item) => {
          // 监听鼠标点击事件
          item.addEventListener("click", (event) => {
            // 阻止默认行为
            event.preventDefault();
            // 遍历所有按钮元素
            buttons.forEach((button) => {
              // 如果是当前点击的会话对应的按钮，则设置为可见状态
              if (button.dataset.lessonId === event.currentTarget.dataset.lessonId) {
                button.style.display = "flex";
                // 否则，设置为隐藏状态
              } else {
                button.style.display = "none";
              }
            });
          });
        });
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.container {
  display: flex;
  width: calc(100% - 260px);
  margin: 0px 40px 0px 270px;
  min-height: 900px;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 260px;
  height: 100%;
  background-color: black;
  color: white;
  padding: 0px;
  padding-inline-start: 0px;
  box-sizing: border-box;
}

.main-content {
  box-sizing: border-box;
  width: 70%;
  margin: 0 auto;
}

.sidebar * {
  color: white;
  font-size: 17px;
}

a {
  text-decoration: none;
}

.sidebar-nav li {
  align-items: center;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 16px;
  list-style: none;
  height: 40px;
  width: 95%;
  display: flex;
  margin: 0px 5px 0px 8px;
  align-items: center;
}

.sidebar-nav li .name {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  left-margin: 30px;
  height: 25px;
  width: 200px;
}
.sidebar-nav li span {
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.sidebar-nav li .fa-home {
  display: inline-flex;
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/shuben1.svg");
  justify-content: center;
  align-items: center;
}

.sidebar-nav li .fas {
  display: inline-flex;
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/dot1.svg");
  justify-content: center;
  align-items: center;
}

.sidebar-nav li .edit {
  display: inline-flex;
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/edit.svg");
  justify-content: center;
  align-items: center;
}
.sidebar-nav li .del {
  display: inline-flex;
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/del.svg");
  justify-content: center;
  align-items: center;
}

.sidebar-nav li .link {
  display: inline-flex;
  text-decoration: none;
  color: inherit;
  width: 100%;
  height: 100%;
  align-items: center;
}

.sidebar-nav li:hover {
  background-color: rgba(245, 245, 245, 0.1);
}

.sidebar-nav li:hover a {
  color: #1e1e1e;
}
.sidebar-header {
  margin: 30px 0px 25px 25px;
}
ul {
  display: block;
  list-style-type: disc;
  margin-block-start: 1em;
  margin-block-end: 1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  padding-inline-start: 0px;
}

.sidebar-nav {
  align-items: center;
  justify-content: center;
}

.sidebar-nav .lesson-actions {
  display: none;
}

.sidebar-nav .lesson-actions .btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  margin: 0px;
  width: 15px;
  height: 25px;
  padding: 0px;
  align-items: center;
  justify-content: center;
  display: inline-flex;
}

.selected .lesson-name {
  display: inline-flex;
  width: calc(100% - 60px) !important;
  align-items: center;
  margin: 0px;
}

.selected {
  background-color: rgba(245, 245, 245, 0.3);
}

.selected .lesson-actions {
  display: inline-flex;
  width: 40px;
  align-items: center;
}
.lessondetail-container {
  width: 100%;
  height: 500%;
}
</style>
