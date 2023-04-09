<template>
  <div class="header">
    <label
      for="lesson-name"
      style="
        margin-left: 10px;
        width: 100px;
        margin-top: 30px;
        align-items: center;
        display: inline-flex;
      "
      >课时名称：</label
    >
    <input
      type="text"
      id="lesson-name"
      v-model="lessonName"
      name="lessonName"
      style="
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1px;
        margin-top: 30px;
        width: 300px;
        height: 30px;
      "
    />
    <el-button type="primary" @click="submit">提交</el-button>
  </div>
  <div class="main-content">
    <QuillEditor
      v-model:content="content"
      :options="editorOption"
      contentType="html"
      ref="myQuillEditor"
      :modules="{ markdownShortcuts: {} }"
    />
  </div>
</template>
<script>
const toolbarOptions = [
  ["bold", "italic", "underline", "strike"],
  ["blockquote", "code-block"],
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }],
  [{ indent: "-1" }, { indent: "+1" }],
  [{ direction: "rtl" }],
  [{ size: ["small", false, "large", "huge"] }],
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  [{ color: [] }, { background: [] }],
  [{ font: [] }],
  [{ align: [] }],
  ["clean"],
  ["link", "image", "video"],
];

import { QuillEditor, Quill } from "@vueup/vue-quill";
import { ImageExtend, QuillWatch } from "quill-image-extend-module";
import quillTool from "@/quillTool";
import QuillMarkdownShortcuts from "quill-markdown-shortcuts";

Quill.register(quillTool, true);
Quill.register("modules/ImageExtend", ImageExtend);

import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";
import myconfig from "../config.js";
import { ElButton } from "element-plus";
// import Delta from 'quill-delta';
import axios from "axios";
export default {
  components: {
    QuillEditor,
    ElButton,
  },
  props: ["model"],
  data() {
    return {
      content: "",
      quill: null,
      editorOption: {
        theme: "snow",
        placeholder: "请输入",
        modules: {
          ImageExtend: {
            name: "file",
            action: myconfig.apiHost + "/lessons/file",
            headers: function (xhr) {
              // 不设置Content-Type，浏览器会自动根据FormData生成multipart/form-data
              xhr.setRequestHeader("s", encodeURIComponent("疯狂星期四v50"));
            },
            processData: false,
            responseType: "json", // 声明响应类型为json
            response: (res) => {
              console.log(res.file_url);
              if (res.file_url) {
                return res.file_url;
              } else {
                throw new Error("上传文件失败");
              }
            },
            size: 8,
            sizeError: () => {
              this.$message.error("粘贴图片大小不能超过8MB!");
            },
          },

          toolbar: {
            container: toolbarOptions,
            handlers: {
              image: function () {
                QuillWatch.emit(this.quill.id);
              },
              link: function (value) {
                if (value) {
                  var href = prompt("请输入链接地址：");
                  this.quill.format("link", href);
                } else {
                  this.quill.format("link", false);
                }
              },
              video: function (value) {
                if (value) {
                  var href = prompt("请输入视频链接：");
                  this.quill.format("video", href);
                } else {
                  this.quill.format("video", false);
                }
              },
              // html: function() {
              //   console.log(this.quill)
              //   return this.quill.root.innerHTML;
              // }
            },
          },
        },
      },
    };
  },
  mounted() {
    this.$nextTick(() => {
      // this.quill = this.$refs.myQuillEditor.getQuill();
      this.quill = this.$refs.myQuillEditor;
      Quill.register("modules/markdownShortcuts", QuillMarkdownShortcuts);
      const container = document.querySelector(".ql-container.ql-snow");
      container.addEventListener("click", function () {
        const editor = document.querySelector(".ql-editor.ql-blank");
        if (editor) {
          editor.focus();
        }
      });

    });
  },
  created() {
    const url = `${myconfig.apiHost}/lessons/${this.$route.params.lesson_id}`;
      axios
        .get(url)
        .then((response) => {
          const data = response.data;
          // const name = data.name;
          const content = data.content;
          // 将获取到的 name 和 content 赋值给对应的变量或者组件的属性
          // this.lessons = response.data;
          this.lessonName = response.data.name;
          this.quill.setContents(content);
          console.log(this.lessonName)
        })
        .catch((error) => {
          console.log(error);
        });
  },
  methods: {
    getContentBlocks() {
      const parser = new DOMParser();
      const htmlDoc = parser.parseFromString(this.quill.getContents(), "text/html");
      const blocks = [];
      let order = 0;
      htmlDoc.querySelectorAll("p, img").forEach((node) => {
        if (node.tagName === "P") {
          blocks.push({
            order: ++order,
            content: node.textContent,
            type: "txt",
          });
        } else if (node.tagName === "IMG") {
          blocks.push({
            order: ++order,
            content: node.src,
            type: "image",
          });
        }
      });
      return blocks;
    },
    submit() {
      // const blocks = this.getContentBlocks();
      // lesson_id: this.$route.params.lesson_id, // TODO: 替换为动态获取的lesson_id
      const blocks = this.quill.getContents();
      const inputElement = document.getElementById("lesson-name");
      const inputValue = inputElement.value;

      const data = {
        name: inputValue,
        content: blocks,
      };
      console.log("data");
      console.log(data); // 调试用，输出请求体内容
      // TODO: 发送POST请求，将data作为请求体
      try {
        const token = localStorage.getItem("token");
        const url = `${myconfig.apiHost}/lessons/${this.$route.params.lesson_id}/edit`; // 构造完整的API地址
        axios.post(url, data, {
          headers: {
            Authorization: `${token}`,
          },
        });
        this.fetchLessons();
      } catch (error) {
        console.error(error);
      }
    },
  },
  // 提交按钮的点击事件处理程序
};
</script>

<style>
.main-content {
  min-height: 600px;
  height: fit-content;
  margin-top: 35px;
}

.ql-container {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px;
  font-size: 14px;
  line-height: 1.5;
  background-color: #fff;
  overflow-y: auto;
  min-height: 600px;
  height: fit-content;
}

.ql-container.ql-blank::before {
  content: attr(data-placeholder);
  color: #a0a0a0;
}

.ql-container.ql-blank .ql-editor::before {
  content: attr(data-placeholder);
  color: #a0a0a0;
  pointer-events: none;
  display: block;
}

.ql-editor pre {
  white-space: pre-wrap;
  font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
  font-size: 13px;
}

.ql-editor .ql-syntax {
  font-size: 13px;
  white-space: pre;
  background-color: #f7f7f7;
  color: #333;
  overflow: visible;
  border-radius: 3px;
  padding: 2px 4px;
  margin: 0 2px;
  font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
}

.ql-editor h1,
.ql-editor h2,
.ql-editor h3,
.ql-editor h4,
.ql-editor h5,
.ql-editor h6 {
  margin: 0;
  font-weight: bold;
}

.ql-editor p {
  margin: 0;
}

.ql-editor a {
  color: #00bfff;
  text-decoration: underline;
}

.ql-editor a:hover {
  color: #0096c9;
  text-decoration: none;
}

.ql-toolbar.ql-snow {
  border: none;
  border-bottom: 1px solid #ccc;
  border-radius: 0px;
  background-color: #f2f2f2;
  height: auto;
}

.ql-toolbar.ql-snow .ql-picker.ql-size .ql-picker-label:before,
.ql-toolbar.ql-snow .ql-picker.ql-size .ql-picker-item:before {
  content: "字体大小";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label:before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item:before {
  content: "标题";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="1"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before {
  content: "大标题";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="2"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="2"]::before {
  content: "中标题";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="3"]::before {
  content: "小标题";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="4"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="4"]::before {
  content: "H4";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="5"]::before {
  content: "H5";
}

.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="6"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before {
  content: "H6";
}

.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-label::before,
.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-item::before {
  content: "标准字体";
}

.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="serif"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="serif"]::before {
  content: "衬线字体";
}

.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-label[data-value="monospace"]::before,
.ql-toolbar.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="monospace"]::before {
  content: "等宽字体";
}

.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item {
  width: 24px;
  height: 24px;
  line-height: 24px;
  border: none;
  padding: 0;
}

.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item.ql-selected svg {
  stroke: #fff;
  stroke-width: 3;
}

.ql-toolbar.ql-snow .ql-picker.ql-background .ql-picker-item {
  width: 24px;
  height: 24px;
  line-height: 24px;
  border: none;
  padding: 0;
}

.ql-toolbar.ql-snow .ql-picker.ql-background .ql-picker-item.ql-selected svg {
  stroke: #fff;
  stroke-width: 3;
}

.ql-toolbar.ql-snow .ql-picker.ql-background .ql-picker-item:not(.ql-selected):hover svg,
.ql-toolbar.ql-snow .ql-picker.ql-background .ql-picker-item:not(.ql-selected):focus svg {
  stroke: #000;
  stroke-width: 1;
}

.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item.ql-selected svg,
.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item[data-value="#000000"] svg,
.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item[data-value="#ffffff"] svg {
  stroke: #fff;
  stroke-width: 3;
}

.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item:not(.ql-selected):hover svg,
.ql-toolbar.ql-snow .ql-picker.ql-color .ql-picker-item:not(.ql-selected):focus svg,
.ql-toolbar.ql-snow
  .ql-picker.ql-color
  .ql-picker-item[data-value="#000000"]:not(.ql-selected):hover
  svg,
.ql-toolbar.ql-snow
  .ql-picker.ql-color
  .ql-picker-item[data-value="#000000"]:not(.ql-selected):focus
  svg,
.ql-toolbar.ql-snow
  .ql-picker.ql-color
  .ql-picker-item[data-value="#ffffff"]:not(.ql-selected):hover
  svg,
.ql-toolbar.ql-snow
  .ql-picker.ql-color
  .ql-picker-item[data-value="#ffffff"]:not(.ql-selected):focus
  svg {
  stroke: #000;
  stroke-width: 1;
}

.el-button {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  background-color: blue;
  border: none;
  padding: 10px 20px;
  color: white;
  font-size: 16px;
  width: 100px;
  margin: 30px 0px 0px 0px;
  position: absolute;
  top: 0;
  right: 0;
}

.header {
  display: inline-flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.ql-container img {
  max-width: 500px;
  max-height: 500px; 
}

</style>
