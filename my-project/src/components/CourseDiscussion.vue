<template>
  <div class="discuss-container">
    <div class="tag-container">
      <div
        class="tag-capsule"
        v-for="(tag, index) in tags"
        :key="index"
        :style="{
          backgroundColor: randomColor(),
          color: fontColor(bgColor),
          width: 'fit-content',
          height: 'fit-content',
          padding: '2px 10px 2px 10px',
          borderRadius: '10px',
          'text-align': 'center',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '5px 10px 5px 10px',
        }"
      >
        {{ tag.name }}
      </div>
    </div>

    <div class="topic-container">
      <div class="topic-card" v-for="(topic, index) in topics" :key="index">
        <div class="topic-info">
          <a>{{ topic.title }}</a>
          <span class="topic-create-time">{{ topic.create_time }}</span>
        </div>

        <div class="topic-comments">
          <a :href="`/topics/${topic.id}/comments`">评论</a>
        </div>
      </div>

      <div v-if="totalPage > 1" class="topic-pagination">
        <a
          class="topic-pagination-link"
          @click="changePage(-1)"
          :class="{ disabled: currentPage === 1 }"
          >&laquo;</a
        >
        <template v-for="page in totalPage" :key="page">
          <a
            class="topic-pagination-link"
            @click="changePage(page)"
            :class="{ active: currentPage === page }"
            >{{ page }}</a
          >
        </template>
        <a
          class="topic-pagination-link"
          @click="changePage(1)"
          :class="{ disabled: currentPage === totalPage }"
          >&raquo;</a
        >
      </div>
    </div>


  </div>
</template>
<script>
import axios from "axios";
import config from "@/config";

export default {
  name: "CourseDiscussion",
  data() {
    return {
      tags: [], // 所有标签
      topics: [], // 所有话题
      bgColor: "",
      currentPage: 1, // 当前页码
      pageSize: 25, // 每页显示的数量
      totalTopics: 0, // 话题总数
      tagColors: {
        // 标签颜色
        primary: "#007bff",
        secondary: "#6c757d",
        success: "#28a745",
        danger: "#dc3545",
        warning: "#ffc107",
        info: "#17a2b8",
        light: "#f8f9fa",
        dark: "#343a40",
      },
    };
  },
  methods: {
    // 获取所有标签
    getTags() {
      const course_id = this.$route.params.id;
      axios.get(`${config.apiHost}/courses/${course_id}/tags`).then((res) => {
        this.tags = res.data.tags;
      });
    },
    // 获取所有话题
    getTopics() {
      const course_id = this.$route.params.id;
      axios
        .get(
          `${config.apiHost}/courses/${course_id}/topics?page=${this.currentPage}&size=${this.pageSize}`
        )
        .then((res) => {
          this.topics = res.data;
          this.totalTopics = parseInt(res.headers["x-total-count"]);
        });
    },
    randomColor() {
      const letters = "0123456789ABCDEF";
      let color = "#";
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      this.bgColor = color;
      return color;
    },
    // 根据标签底色自动调整字体颜色
    fontColor(bgColor) {
      const hexToRgb = (hex) => {
        const rgb = [];
        for (let i = 1; i < 7; i += 2) {
          rgb.push(parseInt(`0x${hex.slice(i, i + 2)}`));
        }
        return rgb;
      };
      const [r, g, b] = hexToRgb(bgColor);
      return r * 0.299 + g * 0.587 + b * 0.114 > 186 ? "#333" : "#fff";
    },

    computed: {
      // 随机标签底色和字体颜色
      tagStyle() {
        return this.tags.map((tag) => {
          // const keys = Object.keys(this.tagColors);
          // const bgColor = this.tagColors[keys[Math.floor(Math.random() * keys.length)]];
          const bgColor = this.randomColor();
          const fontColor = this.fontColor(bgColor);
          return {
            id: tag.id,
            name: tag.name,
            bgColor,
            fontColor,
          };
        });
      },
      changePage(page) {
        if (page === -1 && this.currentPage > 1) {
          this.currentPage -= 1;
        } else if (page === 1 && this.currentPage < this.totalPage) {
          this.currentPage += 1;
        } else if (page >= 1 && page <= this.totalPage) {
          this.currentPage = page;
        }
        this.fetchTopicList(this.currentPage);
      },
      // 点击标签
      clickTag(tag) {
        console.log(tag);
      },
      // 分页变化
      handlePageChange(page) {
        this.currentPage = page;
        this.getTopics();
      },
    },
    // 计算话题的页数
    pageCount() {
      return Math.ceil(this.totalTopics / this.pageSize);
    },
  },
  mounted() {
    this.getTags();
    this.getTopics();
  },
};
</script>

<style>
.tag-container {
  display: flex;
  flex-wrap: wrap;
  padding: 10px 20px 10px 20px;
  margin-top: 100px;
  border: 0.5px solid #ccc;
  border-radius: 20px;
}

.topic-container {
  margin-top: 50px;
}

.topic-card {
  display: flex;
  justify-content: space-between;
  border: 0.5px solid #ccc;
  padding: 10px 10px 10px 10px;
  margin-top: -1px
}

.topic-info {
  display: flex;
  flex-grow: 1;
  flex-direction: column;
}

.topic-create-time {
  color: #999;
  font-size: 10px;
  margin-top: 5px;
}

.topic-comments {
  margin-left: auto;
}
</style>
