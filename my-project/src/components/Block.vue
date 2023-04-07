<template>
  <div>
    <div class="title">
		{{title}}
    </div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title'],
  setup () {
    return {
    }
  }
}
</script>

<style scoped>
.title {
  height: 35px;
}
.content {
  padding: 5px;
}
</style>
