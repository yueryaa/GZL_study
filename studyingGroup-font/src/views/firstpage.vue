<template>
  <div class="top">
    <div class="logo1">
      <img src="../assets/logo.png" alt="logo" class="logo-img" />
      <div class="logo2">
        <span
          v-for="item in logoInfo"
          :key="item.letter"
          :style="{ color: item.color, fontWeight: 'bold' }"
          >{{ item.letter }}</span
        >
      </div>
    </div>
    <div class="user">
      <a href="/logging" class="login-btn">登录 | 注册</a>
    </div>
  </div>
  <div class="main">
    <div class="scroll-images">
      <img src="../assets/slide3.jpg" alt="image" class="img" />
    </div>
    <p
      :style="{
        'font-size': '34px',
        'font-weight': 'bold',
        'text-align': 'center',
        'letter-spacing': '3px',
      }"
    >
      互助学习
    </p>
    <p
      :style="{
        'font-size': '27px',
        'text-align': 'center',
        'letter-spacing': '4px',
        color: '#77787b',
      }"
    >
      让知识传递，让学习更高效
    </p>
    <div class="four-container">
      <div class="row">
        <div class="first">
          <el-icon color="#dea32c" size="50px"><Opportunity /></el-icon>
          <p class="p1">加入群组</p>
          <p class="p2">
            根据专业和兴趣的不同加入不同群组，和志同道合的小伙伴一同学习
          </p>
        </div>
        <div class="second">
          <el-icon color="#45b97c" size="50px"><Memo /></el-icon>
          <p class="p1">分享笔记</p>
          <p class="p2">把自己的学习记录分享在小组，互助学习，交流进步</p>
        </div>
      </div>
      <div class="row">
        <div class="third">
          <el-icon color="#6f60aa" size="50px"><Finished /></el-icon>
          <p class="p1">点赞收藏</p>
          <p class="p2">点赞收藏对自己有帮助的学习记录，可随时查看方便快捷</p>
        </div>
        <div class="fourth">
          <el-icon color="#ef5b9c" size="50px"><TrendCharts /></el-icon>
          <p class="p1">组内排名</p>
          <p class="p2">根据组内点赞排行榜和发帖排行榜，提升学习积极性</p>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <p>&copy; 2023 All rights reserved.</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

//图标与颜色
const logoInfo = ref([
  {
    letter: "S",
    color: "#3285FF",
  },
  {
    letter: "t",
    color: "#FB3624",
  },
  {
    letter: "u",
    color: "#FFBA02",
  },
  {
    letter: "d",
    color: "#3285FF",
  },
  {
    letter: "y",
    color: "#25B24E",
  },
  {
    letter: "G",
    color: "#FD3224",
  },
  {
    letter: "r",
    color: "#FFBA02",
  },
  {
    letter: "o",
    color: "#3285FF",
  },
  {
    letter: "u",
    color: "#25B24E",
  },
  {
    letter: "p",
    color: "#FFBA02",
  },
]);
</script>

<style lang="scss" scoped>
/* top栏样式 */
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  background-color: #fff;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.2);
}
.logo1 {
  display: flex;
  width: 500px;
}
.logo-img {
  margin-left: 100px;
  margin-right: 10px;
  width: 40px;
  height: 40px;
}
.logo2 {
  margin-right: 5px;
  font-size: 30px;
}

.user {
  margin-right: 200px;
}

.login-btn,
.register-btn {
  text-decoration: none;
  margin-left: 20px;
  display: inline-block;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  color: #fff;
  background-color: #007bff;
  cursor: pointer;
}

.login-btn:hover,
.register-btn:hover {
  background-color: #0062cc;
}

/* main区域样式 */
.main {
  align-items: center;
  margin-bottom: 30px;
  .four-container {
    margin-left: 350px;
    width: 1100px;
    height: 500px;
    background-color: #f7fdff;
    border: 3px solid #ffffff;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    width: 100%;
  }

  .first,
  .second,
  .third,
  .fourth {
    width: 48%;
    display: flex;
    margin-top: 30px;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .p1 {
    font-size: 20px;
    font-weight: bold;
    letter-spacing: 4px;
  }
  .p2 {
    font-size: 17px;
    color: #72777b;
    letter-spacing: 4px;
  }
}

.img {
  width: 100%; /* 图片占满容器宽度 */
  height: auto; /* 自适应高度 */
}

/* footer区域样式 */
.footer {
  background-color: #5a5a5a;
  text-align: center;
  padding: 20px;
  font-size: 14px;
  color: #a1a1a1;
}
</style>
