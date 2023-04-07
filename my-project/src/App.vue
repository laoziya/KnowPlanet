<template>
  
  <div class="f-container">
    <div class="f-main-content">
      <!-- 主要内容区域 -->
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>


<style>

.f-container {
  display: flex;
  justify-content: center;
}

.f-main-content {
  width: 100%;
  height: fit-content;
  background-color: #fff;
  padding: 20px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

</style>