<template>
  <div class="discuss-container">
    <div class="tag-container">
      <div
        class="tag-capsule"
        v-for="(tag, index) in tags"
        :key="index"
        :style="{
          backgroundColor: tag.bgColor,
          color: tag.fontColor,
        }"
        @click="addFilterTag(tag)"
      >
        {{ tag.name }}

        <button
          v-show="tagEditing"
          class="del-tag-btn"
          @click="onDeleteTag(tag.id)"
          :style="{
            color: tag.fontColor,
          }"
        >
          ×
        </button>
      </div>

      <div class="create-tag">
        <input
          type="text"
          placeholder="新建标签"
          class="tag-input"
          v-model="tagName"
          @keydown.enter="createTag"
        />
        <button class="create-tag-btn" @click="createTag">
          <i class="create-tag-icon" />
        </button>
      </div>

      <button class="edit-button" @click="onEditTags(tag)">
        {{ editButtonText }}
      </button>
    </div>

    <div class="topic-container">
      <div class="topic-card lable-filter" v-if="tag_all">
        <div
          class="tag-capsule"
          v-for="(tag, index) in filterTags"
          :key="index"
          :style="{
            backgroundColor: tag.bgColor,
            color: tag.fontColor,
          }"
        >
          {{ tag.name }}

          <button
            class="del-tag-btn"
            @click="removeTagFromFilter(tag.id)"
            :style="{
              color: tag.fontColor,
            }"
          >
            ×
          </button>
        </div>
      </div>

      <div class="topic-card" v-for="(topic, index) in topics" :key="index">
        <div class="topic-info">
          <a class="topic-title">{{ topic.title }}</a>
          <span class="topic-create-time">{{ topic.create_time }}</span>
        </div>

        <div class="labels">
          <a @click="showLabelWindow(topic.id)">
            <i class="labels_icon"></i>
            labels
          </a>
        </div>
        <div class="topic-comments">
          <a :href="`/topics/${topic.id}/comments`"><i class="comment-icon"/></a>
        </div>

        <div
          v-if="showLabel"
          class="label-window"
          :style="{
            position: 'absolute',
            top: labelWindowPosition.y + 'px',
            left: labelWindowPosition.x + 'px',
          }"
        >
          <!-- label window content -->
          此Topic的标签
          <div
            class="tag-capsule"
            v-for="(tag, index) in currentTopicTags"
            :key="index"
            :style="{
              backgroundColor: tag.bgColor,
              color: tag.fontColor,
            }"
          >
            {{ tag.name }}
            <button
              class="del-tag-btn"
              @click="onDeleteFromTopicTag(tag.id)"
              :style="{
                color: tag.fontColor,
              }"
            >
              ×
            </button>
          </div>
          <div class="create-tag">
            <input
              type="text"
              placeholder="添加标签到此Topic"
              class="tag-input"
              v-model="tagName"
              @keydown.enter="addTagToTopic"
            />
            
          </div>
        </div>
        <div class="del-topic" @click="delTopic(topic.id)">
          <i class="del-topic-icon" />
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

      <div class="create-topic">
        <input
          class="topic-input"
          type="text"
          placeholder="输入话题名称"
          @keyup.enter="createTopic"
        />
        <button class="create-topic-btn" @click="createTopic">创建</button>
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
      filterTags: [],
      bgColor: "",
      currentTopicTags: [],
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
      tagEditing: false,
      editButtonText: "编辑标签",
      showLabel: false,
      labelWindowPosition: { x: 0, y: 0 },
    };
  },
  methods: {
    // 获取所有标签
    getTags() {
      const course_id = this.$route.params.id;
      axios.get(`${config.apiHost}/courses/${course_id}/tags`).then((res) => {
        this.tags = res.data.tags.map((tag) => {
          const bgColor = this.randomColor();
          const fontColor = this.fontColor(bgColor);
          return {
            id: tag.id,
            name: tag.name,
            bgColor: bgColor,
            fontColor: fontColor,
          };
        });
        const bgColor = this.randomColor();
        const fontColor = this.fontColor(bgColor);
        this.tag_all = {
          id: 0,
          name: "all",
          bgColor: bgColor,
          fontColor: fontColor,
        };
        this.tags.unshift(this.tag_all);
        this.filterTags.push(this.tag_all);
      });
    },
    getTopicTags(topic_id) {
      axios.get(`${config.apiHost}/topics/${topic_id}/tags`).then((res) => {
        this.currentTopicTags = res.data.map((tag) => {
          const bgColor = this.randomColor();
          const fontColor = this.fontColor(bgColor);
          return {
            id: tag.id,
            name: tag.name,
            bgColor: bgColor,
            fontColor: fontColor,
          };
        });
        const bgColor = this.randomColor();
        const fontColor = this.fontColor(bgColor);
        this.currentTopicTags.unshift({
          id: 0,
          name: "all",
          bgColor: bgColor,
          fontColor: fontColor,
        });
      });
    },

    addFilterTag(tag) {
      this.filterTags.push(tag);
    },

    removeTagFromFilter(tagId) {
      this.filterTags = this.filterTags.filter((tag) => tag.id !== tagId);
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
    // getTopicTags(topic_id) {
    //   axios
    //     .get(`${config.apiHost}/topics/${topic_id}/tags`)
    //     .then((response) => {
    //       this.currentTopicTags = response.data.tags;
    //     })
    //     .catch((error) => {
    //       console.log(`Error: ${error}`);
    //     });
    // },
    async createTag() {
      const name = document.querySelector(".tag-input").value;
      const course_id = this.$route.params.id;
      const data = { course_id: course_id, name: name };
      const token = localStorage.getItem("token");
      const response = await fetch(`${config.apiHost}/courses/tags`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `${token}` },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (response.ok) {
        this.getTags();
        //清空输入框
        this.tagName = "";
      } else {
        const message = result.error || "创建失败";
        alert(message);
      }
    },

    onDeleteTag(tagId) {
      const token = localStorage.getItem("token");
      axios
        .delete(`${config.apiHost}/tags/${tagId}`, {
          headers: {
            Authorization: token,
          },
        })
        .then((res) => {
          console.log(res.data);
          // 成功删除后重新加载标签
          this.getTags();
        })
        .catch((err) => {
          console.log(err);
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
    onEditTags() {
      if (this.tagEditing) {
        // 处理取消编辑的逻辑
        this.tagEditing = false;
        this.editButtonText = "编辑标签";
      } else {
        // 处理编辑标签的逻辑
        this.tagEditing = true;
        this.editButtonText = "取消编辑";
      }
    },

    async createTopic() {
      const title = document.querySelector(".topic-input").value;
      const course_id = this.$route.params.id;
      const data = { course_id: course_id, title: title, content: "" };
      const token = localStorage.getItem("token");
      const response = await fetch(`${config.apiHost}/topics/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `${token}` },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (response.status === 201) {
        console.log(`已创建${title}话题`);
        document.querySelector(".topic-input").value = ""; // 创建成功后清空输入框
        this.getTopics(); // 创建成功后刷新话题列表
      } else {
        const errorMessage = result.error ? result.error : "创建失败";
        console.log(errorMessage);
      }
    },

    async delTopic(topicId) {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`${config.apiHost}/topics/${topicId}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        });
        if (response.status === 200) {
          console.log(`Topic ${topicId} deleted successfully`);
          // 删除话题后，需要重新获取话题列表
          this.getTopics();
        } else {
          console.log(`Failed to delete topic ${topicId}`);
          const result = await response.json();
          const message = result?.error || "Delete topic failed";
          alert(message);
        }
      } catch (error) {
        console.log(`Failed to delete topic ${topicId}`);
        console.error(error);
        alert("Delete topic failed");
      }
    },

    showLabelWindow(topic_id) {
      this.showLabel = !this.showLabel;
      this.labelWindowPosition = { x: event.clientX - 80, y: event.clientY - 220 };
      event.currentTarget.classList.toggle("clicked");
      this.currentTopicId = topic_id;
      this.getTopicTags(topic_id);
    },
    async addTagToTopic() {
      const tagName = this.tagName.trim();
      if (!tagName) {
        return;
      }
      const tag = this.tags.find((t) => t.name === tagName);
      if (!tag) {
        alert(`标签"${tagName}"不存在，请先创建该标签`);
        return;
      }
      const topicId = this.currentTopicId;
      const tagId = tag.id;
      const token = localStorage.getItem("token");
      try {
        const response = await axios.post(
          `${config.apiHost}/topics/${topicId}/tags/${tagId}`,
          null,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: token,
            },
          }
        );
        console.log(response.data);
        // 添加成功后，重新获取话题的标签列表
        this.getTopicTags(topicId);
      } catch (error) {
        console.log(error);
        alert("添加标签失败");
      }
      this.tagName = "";
    },

    onDeleteFromTopicTag(tagId) {
      const token = localStorage.getItem("token");
      axios
        .delete(`${config.apiHost}/topics/${this.currentTopicId}/tag/${tagId}`, {
          headers: { Authorization: `${token}` },
        })
        .then(() => {
          // 在前端删除此标签
          const tagIndex = this.currentTopicTags.findIndex((tag) => tag.id === tagId);
          if (tagIndex !== -1) {
            this.currentTopicTags.splice(tagIndex, 1);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    computed: {
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
  created() {
    this.$watch(
      "filterTags",
      (newVal) => {
        if (newVal.length === 0) {
          this.getTopics();
          return;
        }
        if (newVal.length === 1 && newVal[0].id === 0) {
          this.getTopics();
          return;
        }

        // 构造请求 URL
        let url = `${config.apiHost}/topics/search-by-tags`;
        let tagIds = newVal
          .filter((tag) => tag.id !== 0)
          .map((tag) => `tag_id=${tag.id}`)
          .join("&");
        if (tagIds) {
          url += `?${tagIds}`;
        }

        // 发送请求获取 topics 数据
        axios
          .get(url)
          .then((response) => {
            this.topics = response.data.topics;
          })
          .catch((error) => {
            console.log(error);
          });
      },
      { deep: true }
    );
  },
};
</script>

<style>
/*标签容器*/
.tag-container {
  display: flex;
  flex-wrap: wrap;
  padding: 10px 20px 10px 20px;
  margin-top: 100px;
  border: 0.5px solid #ccc;
  border-radius: 20px;
}

/*标签*/
.tag-capsule {
  width: fit-content;
  height: fit-content;
  padding: 2px 10px 2px 10px;
  border-radius: 10px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 5px 10px 5px 10px;
  transition: transform 0.2s ease-in-out; /* 添加过渡效果 */
  user-select: none; /* 禁止光标变成输入形式 */
}

.tag-capsule:hover {
  transform: scale(1.1); /* 鼠标移到时将标签放大 10% */
}

/*创建新标签的容器*/
.create-tag {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin: 0px 100px 0px 10px;
  height: fit-content;
}
/*输入标签名的容器*/
.tag-input {
  height: 30px;
  background-color: transparent;
  border: none;
}
.tag-input:focus {
  outline: none;
  border: none;
  box-shadow: none;
}
/*新建标签按钮*/
.create-tag-btn {
  align-items: center;
  border: none;
  height: 100%;
  background-color: transparent;
  display: flex;
}
/*新建标签图标*/
.create-tag-icon {
  display: inline-flex;
  width: 15px;
  height: 15px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/createtag3.svg");
  justify-content: center;
  align-items: center;
}
/*编辑标签按钮*/
.edit-button {
  background-color: blue;
  color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px 10px;
  height: fit-content;
}

.del-tag-btn {
  background-color: transparent;
  border: none;
  width: 15px;
  height: 15px;
}
/*话题容器*/
.topic-container {
  margin-top: 50px;
}

.topic-container .tag-capsule {
  font-size: 10px;
}
/*话题*/
.topic-card {
  display: flex;
  justify-content: space-between;
  border: 0.5px solid #ccc;
  padding: 10px;
  margin-top: -1px;
  justify-content: flex-start;
}

/*话题标题和创建日期的容器*/
.topic-info {
  display: flex;
  flex-direction: column;
  flex: 1 0 65%;
}

/*话题创建日期字体*/
.topic-create-time {
  color: #999;
  font-size: 10px;
  margin-top: 5px;
}

/*topic中显示的标签按钮容器*/
.labels {
  display: flex;
  flex: 1 0 15%;
  margin-right: 5%;
  outline: none;
  margin-left: auto;
  align-items: center;
}

/*标签按钮容器中的a标签*/
.labels a {
  display: flex;
  align-items: center;
  outline: none;
}

.labels a.clicked {
  font-size: 16px;
  font-weight: bold;
  color: blue;
}

/*标签按钮图标*/
.labels_icon {
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/lable.svg");
  margin: 5px;
}

/*评论*/
.topic-comments {
  display: flex;
  flex: 1 0 10%;
  margin-left: auto;
  align-items: center;
}

.comment-icon {
  display: flex;
  width: 18px;
  height: 18px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/comment1.svg");
  margin: 5px;
},

.topic-container .lable-filter {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.del-topic {
  display: flex;
  flex: 1 0 5%;
  margin-left: auto;
  align-items: center;
}

.del-topic-icon {
  display: flex;
  width: 15px;
  height: 14px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url("../assets/del.svg");
}

/*创建话题*/
.create-topic {
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  align-items: center;
  border-radius: 20px;
  margin-top: 40px;
}

.topic-input {
  height: 100%;
  background-color: transparent;
  border: none;
  border-radius: 5px;
  padding: 5px;
  margin-right: 10px;
  flex: 1 0 75%;
}

.topic-input:focus {
  outline: none;
  border: none;
  box-shadow: none;
}

.create-topic-btn {
  background-color: transparent;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  flex: 1 0 25%;
}

.labels {
  position: relative;
  z-index: 1; /* 保证在其他元素之上 */
}
.label-window {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 50px; /* 距离页面顶部的距离 */
  left: 0;
  width: 200px;
  height: 200px;
  background-color: #fff;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  z-index: 2; /* 覆盖在其他元素之上 */
}
.label-window .create-tag {
  width: 80%;
}
</style>
