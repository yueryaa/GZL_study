<template>
  <div class="header-content-home">
    <div class="user-banner">
      <a @click="gotoHomePage" style="color: #3285ff">首页</a>
      <span>&nbsp;&nbsp;>&nbsp;&nbsp;个人中心</span>
    </div>
    <div class="contioner">
      <div class="ucenter-panel">
        <div class="user-side">
          <div v-if="userExists">
            <div class="avatar-panel">
              <div class="edit-btn a-link" @click="goToEdit">修改资料</div>
              <div class="avater-inner">
                <el-avatar :size="100" :src="avaterpicture"></el-avatar>
                <!-- <image src ='../assets/default-image.jpg' class="img" :style="{'margin-left':'80px'}"></image> -->
              </div>
              <div class="nick-name">
                <span>{{ userInfo.name }}</span>
                <span
                  v-if="userInfo.sex == '女'"
                  class="iconfont icon-woman"
                  :style="{ color: 'pink' }"
                ></span>
                <span
                  v-if="userInfo.sex == '男'"
                  class="iconfont icon-man"
                  :style="{ color: 'blue' }"
                ></span>
              </div>
              <div class="desc">
                <div v-if="userInfo.remark">{{ userInfo.remark }}</div>
                <div v-else>这个人很懒没有留下备注</div>
              </div>
            </div>
            <!--关注 点赞信息-->
            <div class="user-extend-panel">
              <div class="info-item">
                <div class="label iconfont icon-integral">积分</div>

                <div class="value">
                  {{
                    userInfo.likeCount * 1 +
                    userInfo.postCount * 2 +
                    userInfo.collectCount * 1
                  }}
                </div>
              </div>
              <div class="info-item">
                <div class="label iconfont icon-like">获赞</div>

                <div class="value">{{ userInfo.likeCount }}</div>
              </div>
              <div class="info-item">
                <div class="label iconfont icon-post">发帖</div>

                <div class="value">{{ userInfo.postCount }}</div>
              </div>
              <div class="info-item">
                <div class="label iconfont icon-login">收藏</div>

                <div class="value">{{ userInfo.collectCount }}</div>
              </div>
            </div>
          </div>
          <div v-else>
            <!-- 当用户不存在时显示的内容 -->
            <p v-show="loading" class="loading-text">拼命加载中</p>
          </div>
        </div>
        <div class="artical-panel"></div>
      </div>

      <!--文章列表栏-->
      <div class="all-lists">
        <el-tabs type="border-card">
          <el-tab-pane label="发布">
            <div class="post-lists">
              <div v-if="ownartical == null || ownartical.length == 0">
                <noData :msg="msg"></noData>
              </div>
              <div v-else>
                <div
                  v-for="(data, index) in ownartical"
                  :key="data.aid"
                  class="post-items"
                >
                  <ArticalList
                    :data="data"
                    :gid="data.gid"
                    mode="first"
                    :isliked="isliked[index]"
                    :iscollected="iscollected[index]"
                    @update:ownartical="handleUpdateOwnartical"
                  ></ArticalList>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="收藏">
            <div class="post-lists">
              <div
                v-if="
                  owncollectartical == null || owncollectartical.length == 0
                "
              >
                <noData :msg="msg"></noData>
              </div>
              <div v-else>
                <div
                  v-for="data in owncollectartical"
                  :key="data.aid"
                  class="post-items"
                >
                  <ArticalList
                    :data="data"
                    :gid="data.gid"
                    mode="third"
                    @update:owncollectartical="handleUpdateOwncollectartical"
                  ></ArticalList>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="点赞">
            <div class="post-lists">
              <div v-if="ownlikeartical == null || ownlikeartical.length == 0">
                <noData :msg="msg"></noData>
              </div>
              <div v-else>
                <div
                  v-for="data in ownlikeartical"
                  :key="data.aid"
                  class="post-items"
                >
                  <ArticalList
                    :data="data"
                    :gid="data.gid"
                    mode="second"
                    @update:ownlikeartical="handleUpdateOwnlikeartical"
                  ></ArticalList>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import qs from "querystring";

import { inject } from "vue";
import ArticalList from "./Arcitals/ArticalList.vue";
import noData from "./Arcitals/nodata.vue";

const axios = inject("axios");
const globalTarget = inject("globalTarget");
const router = useRouter();
const route = useRoute();
const uid = route.params.uid;
const userInfo = ref({}); // 初始化为空对象，避免 undefined 错误
const userExists = ref(false); // 用于标识用户是否存在
const loading = ref(true);
const msg = "空空如也";
const avaterpicture = ref();
const pictureData = ref();
//回到首页
function gotoHomePage() {
  router.push(`/${uid}`);
}
//获取用户信息
async function fetchUserInfo(userId) {
  try {
    const targetUrl = globalTarget + "UserDetail/";
    const response = await axios.get("/UserDetail/", { params: { id: uid } });
    userInfo.value = response.data;
    userExists.value = true; // 用户存在
    console.log("用户信息", response);
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // 如果API返回404错误，意味着用户不存在
      userExists.value = false;
    } else {
      // 其他错误处理
      console.error("获取用户信息失败:", error);
    }
  }
}
//修改个人资料
const goToEdit = () => {
  router.push(`/edit/${uid}`);
};

// const isCollected = inject('isCollected');
// const resultcollect = isCollected();
// const isLiked = inject('isLiked');
// const resultlike = isCollected();
const iscollected = ref([]);
function isCollected_user() {
  const length = ownartical.value.length;
  iscollected.value = Array.from({ length }, () => false);
  for (let i = 0; i < ownartical.value.length; i++) {
    let collectlist = [];

    collectlist = ownartical.value[i].favoritesList;

    for (let j = 0; j < collectlist.length; j++) {
      if (collectlist[j].uid == uid) {
        iscollected.value[i] = true;
      }
    }
  }
  console.log(iscollected);
}

const isliked = ref([]);
function isLiked_user() {
  const length = ownartical.value.length;
  isliked.value = Array.from({ length }, () => false);
  for (let i = 0; i < ownartical.value.length; i++) {
    let likelist = [];
    likelist = ownartical.value[i].likeList;

    for (let j = 0; j < likelist.length; j++) {
      if (likelist[j].uid == uid) {
        isliked.value[i] = true;
      }
    }
  }

  console.log(isliked.value);
}
//发布帖子
const ownartical = ref([]);
async function fetchOwnArticalInfo(userId) {
  try {
    const responseartical = await axios.get("/getownArtical/", {
      params: { id: uid },
    });
    isCollected_user();
    isLiked_user();
    ownartical.value = responseartical.data;
    console.log("文章信息", ownartical.value);
  } catch (error) {
    console.error("获取文章信息失败:", error);
  }
}
function handleUpdateOwnartical(updatedData) {
  console.log("updata", updatedData);
  console.log("origian", ownartical.value);
  ownartical.value = updatedData;
  console.log("origian", ownartical.value);
}

//收藏帖子
const owncollectartical = ref([]);
async function fetchOwncollectArticalInfo(userId) {
  try {
    const collectartical = await axios.get("/getowncollectArtical/", {
      params: { id: uid },
    });
    owncollectartical.value = collectartical.data;
    console.log("文章信息", owncollectartical.value);
  } catch (error) {
    console.error("获取文章信息失败:", error);
  }
}
function handleUpdateOwncollectartical(updatedData) {
  console.log("updata", updatedData);
  console.log("origian", owncollectartical.value);
  owncollectartical.value = updatedData;
  console.log("origian", owncollectartical.value);
}

//点赞帖子
const ownlikeartical = ref([]);
async function fetchOwnlikeArticalInfo(userId) {
  try {
    const likeartical = await axios.get("/getownlikeArtical/", {
      params: { id: uid },
    });
    ownlikeartical.value = likeartical.data;
    console.log("文章信息", likeartical);
  } catch (error) {
    console.error("获取文章信息失败:", error);
  }
}
function handleUpdateOwnlikeartical(updatedData) {
  console.log("updata", updatedData);
  console.log("origian", ownlikeartical.value);
  ownlikeartical.value = updatedData;
  console.log("origian", ownlikeartical.value);
}
function fectchavaterpicture(uid) {
  axios.get("/file/getAvatar/", { params: { id: uid } }).then((pictureRes) => {
    pictureData.value = pictureRes.data;
    console.log(pictureData);
    avaterpicture.value = pictureData.value.picture;
    console.log(avaterpicture);
  });
}

// 在组件挂载时调用函数
onMounted(() => {
  console.log(uid);
  if (uid) {
    fectchavaterpicture(uid);
    fetchUserInfo(uid);
    fetchOwnArticalInfo(uid);
    fetchOwncollectArticalInfo(uid);
    fetchOwnlikeArticalInfo(uid);
  }
});
</script>



<style lang="scss" scoped>
.header-content-home {
  margin-top: 70px;
  margin-left: 45px;
  .user-banner {
    //font-size: 20px;
    color: #9ba7b9;
  }
  .contioner {
    display: flex;
    height: 1000px;
    .ucenter-panel {
      flex-basis: 20%;
      display: flex;
      .user-side {
        width: 300px;
        margin-right: 10px;
        .avatar-panel {
          margin: 10px;
          background: #fff;
          box-shadow: 0 2px 6px 0 #ddd;
          text-align: center;
          padding: 10px;
          .edit-btn {
            text-align: right;
            font-size: 15px;
            color: #3285ff;
          }
          .avater-inner {
            display: flex;
            justify-content: center;
            .img {
              width: 120px;
              height: 120px;
              border-radius: 60px;
            }
          }
          .nick-name {
            .iconfont {
              margin-left: 5px;
              color: var(--link);
            }
          }
          .desc {
            margin-top: 5px;
            text-align: left;
            font-size: 14px;
            color: #91b7ef;
          }
        }
        .user-extend-panel {
          margin-top: 10px;
          background: #fff;
          box-shadow: 0 2px 6px 0 #ddd;
          padding: 8px;
          .info-item {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            .label {
              font-size: 13px;
            }
            .label::before {
              font-size: 22px;
              color: #888888;
              padding-right: 10px;
            }
          }
        }
      }
      .artical-panel {
        flex: 1;
      }
    }
    .all-lists {
      flex-basis: 80%;
      margin-right: 50px;
      margin-left: 25px;
      height: 1000px;
      background-color: #fff;
      box-shadow: 2px 2px 3px 2px #ddd;
      .post-lists {
        overflow: auto;
      }

      .post-item {
        background-color: #f6f6f9;
        padding: 10px;
        margin-bottom: 15px;
      }
    }
  }
}
</style>
