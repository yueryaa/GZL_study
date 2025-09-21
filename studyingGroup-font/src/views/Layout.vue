<template>
  <div>
    <div class="header" v-if="showHeader">
      <div class="header-content" :style="{ width: '1600px' }">
        <img src="../assets/logo.png" alt="logo" class="logo-img" />
        <div class="logo">
          <span
            v-for="item in logoInfo"
            :key="item.letter"
            :style="{ color: item.color, fontWeight: 'bold' }"
            >{{ item.letter }}</span
          >
        </div>
        <!--板块信息-->
        <div class="menue-panel"></div>
        <!--用户头像-->
        <div class="user-info-panel">
          <el-button type="primary" class="opt-btn" @click="gotoWritePost">
            发帖<span class="iconfont icon-add"></span>
          </el-button>
          <div class="user">
            <el-dropdown>
              <el-avatar :src="imageurl" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToHome"
                    >我的主页</el-dropdown-item
                  >
                  <el-dropdown-item @click="goToEdit"
                    >修改信息</el-dropdown-item
                  >
                  <el-dropdown-item @click="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
    </div>
    <div class="body-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import store from "../store";
import { inject } from "vue";
const axios = inject("axios");

const router = useRouter();

// 定义响应式变量
const showHeader = ref(true);
const account = ref(null); // 使用 ref 创建响应式变量
const imageurl = ref();
const pictureData = ref();

// 获取并监听滚动事件
const getScrollTop = () => {
  let scrollTop =
    document.documentElement.scrollTop ||
    window.pageYOffset ||
    document.body.scrollTop;
  return scrollTop;
};

const initScroll = () => {
  let initScrollTop = getScrollTop();
  let scrollType = 0;
  window.addEventListener("scroll", () => {
    let currentScrollTop = getScrollTop();
    if (currentScrollTop > initScrollTop) {
      // 向下滚动
      scrollType = 1;
    } else {
      // 向上滚动
      scrollType = 0;
    }
    initScrollTop = currentScrollTop;
    if (scrollType == 1 && currentScrollTop > 60) {
      showHeader.value = false;
    } else {
      showHeader.value = true;
    }
  });
};
const accountStr = localStorage.getItem("uid");
onMounted(() => {
  initScroll();
  // 在组件挂载后从localStorage中读取account信息
  const accountStr = localStorage.getItem("uid");
  if (accountStr) {
    console.log(typeof accountStr, accountStr);
  }
  try {
    axios
      .get("/file/getAvatar/", { params: { id: accountStr } })
      .then((pictureRes) => {
        pictureData.value = pictureRes.data;
        console.log(pictureData);
        imageurl.value = pictureData.value.picture;
        console.log(imageurl);
      });
  } catch (error) {
    console.error("An error occurred:", error);
  }
});
//监听 登陆用户信息
const userInfo = ref({});
//按钮跳转
const goToHome = () => {
  const uid = accountStr;
  router.push(`/home/${uid}`);
};

const goToEdit = () => {
  const uid = parseInt(accountStr); // 替换为正确的 ID
  router.push(`/edit/${uid}`);
};

const logout = () => {
  store.state.isLogin = false;
  router.push("/logging");
};
//发帖
function gotoWritePost() {
  const uid = parseInt(accountStr);
  router.push(`/${uid}/writepost`);
}

//修改默认图像
const imageSrc = ref("");
const defaultImageSrc = "../assets/default-image.jpg"; // 默认图片地址

const handleImageError = () => {
  imageSrc.value = defaultImageSrc; // 加载失败时，使用默认图片
};
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
.header {
  top: 0px;
  width: 100%;
  height: 60px;
  position: fixed;
  box-shadow: 0 2px 6px 0 #ddd;
  background: white;
  .header-content {
    align-items: center;
    margin: 0px auto;
    height: 60px;
    display: flex;
    .logo {
      display: block;
      margin-right: 5px;
      font-size: 30px;
    }
    .logo-img {
      margin-right: 10px;
      width: 40px;
      height: 40px;
    }
    .menue-panel {
      flex: 1;
    }
    .user-info-panel {
      width: 450px;
      display: flex; /* 使用Flexbox布局 */
      align-items: center; /* 垂直居中对齐子元素 */
      justify-content: space-between; /* 子元素之间保持等距离分布 */
      //background: red;

      .opt-btn {
        margin-left: 310px;
        flex: none;
        .iconfont {
          margin-left: 5px;
        }
      }
      .user-info {
        flex-grow: 1;
        padding: 10px;
        .item {
          .icon-message {
            font-size: 25px;
          }
        }
      }
    }
  }
}
</style>
