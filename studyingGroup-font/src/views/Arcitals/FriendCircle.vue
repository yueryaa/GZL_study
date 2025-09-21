<template>
  <div>
    <div class="friendcircle-content">
      <!--返回建-->
      <div class="user-banner">
        <a @click="gotoHomePage" style="color: #3285ff">首页</a>
        <span>&nbsp;&nbsp;>&nbsp;&nbsp;朋友圈</span>
      </div>

      <!--小组栏-->
      <div class="main-list">
        <!--小组栏-->
        <div class="group-list">
          <div class="group-message">
            <img src="../../assets/group.png" class="avatar" />
            <div :style="{ 'margin-left': '10px' }">{{ groupData }}小组</div>
            <span
              class="iconfont icon-open"
              :style="{ transform: 'rotate(90deg)', 'margin-left': '35px' }"
            ></span>
          </div>
        </div>
        <!--文章栏-->
        <div class="artical-list">
          <!--头像与名字-->
          <div class="post-lists">
            <div
              v-for="(data, index) in articalData"
              :key="data.aid"
              class="post-item"
            >
              <div class="post-content">
                <img :src="data.picture" alt="image" class="image" />
                <div class="user-info">
                  <div class="user-name">{{ data.name }}</div>
                </div>
                <div v-if="data.uid == uid">
                  <el-dropdown :style="{ 'margin-left': '870px' }">
                    <span class="el-dropdown-link">
                      <el-icon><MoreFilled /></el-icon>
                    </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item
                          @click="deleteownArticalClick(data.aid)"
                          >删除该动态</el-dropdown-item
                        >
                        <el-dropdown-item @click="editArticalClick(data.aid)"
                          >修改该动态</el-dropdown-item
                        >
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>

              <!--文章内容-->
              <div class="content">
                {{ data.content }}
                <div class="content-image">
                  <div
                    v-for="(img, i) in imageurls[index]"
                    :key="i"
                    class="image-wrapper"
                  >
                    <el-image
                      style="width: 300px; height: 200px"
                      :src="img"
                      fit="cover"
                      @error="handleError"
                      :preview-src-list="imageurls[index]"
                    >
                      <template #error>
                        <div class="image-slot">
                          <el-icon name="el-icon-picture" />
                        </div>
                      </template>
                    </el-image>
                  </div>
                </div>

                <!--文章时间与图标-->
              </div>
              <div class="icon-time-style">
                <div class="atime">{{ data.atime }}</div>
                <div class="icons">
                  <span
                    v-if="isliked[index]"
                    class="iconfont icon-good"
                    :style="{ color: '#f05b72', 'font-size': '20px' }"
                    @click="likeArticalClick(data.aid, index)"
                  ></span>
                  <span
                    v-else
                    class="iconfont icon-like"
                    :style="{ color: '#f05b72', 'font-size': '20px' }"
                    @click="likeArticalClick(data.aid, index)"
                  ></span>

                  <span
                    v-if="iscollected[index]"
                    class="iconfont icon-user-filling"
                    :style="{ color: '#FFBA02' }"
                    @click="collectArticalClick(data.aid, index)"
                  ></span>
                  <span
                    v-else
                    class="iconfont icon-empty"
                    :style="{ color: '#FFBA02' }"
                    @click="collectArticalClick(data.aid, index)"
                  ></span>

                  <span
                    class="iconfont icon-comment"
                    :style="{ color: '#78a355' }"
                    @click="commentArticalClick(data.aid)"
                  ></span>
                  <!--只有管理员可以删-->
                  <span
                    v-if="isadmin == 1"
                    class="iconfont icon-del"
                    :style="{ color: '#2b4490' }"
                    @click="deleteArticalClick(data.aid)"
                  ></span>
                </div>
              </div>

              <!--文章点赞与评论-->
              <div class="like-list">
                <span
                  class="iconfont icon-good"
                  :style="{ color: '#f05b72' }"
                  v-if="data.likeList.length > 0"
                ></span>
                {{ data.likeList.map((item) => item.name).join(", ") }}
              </div>
              <div class="comment-list">
                <div
                  v-for="(comment, cIndex) in data.commentList"
                  :key="cIndex"
                >
                  <div class="commenter">
                    <el-icon color="#78a355"><UserFilled /></el-icon>
                    {{ comment.name }}:
                  </div>
                  <div class="comment">{{ comment.content }}</div>
                </div>
              </div>
              <hr v-if="index !== articalData.length - 1" class="divider" />
            </div>
          </div>
        </div>
        <!--排行榜-->
        <div class="ranking-list">
          <div class="title-rank">
            <img src="../../assets/rank0.png" alt="Rank 0" class="rank0-img" />
          </div>
          <el-tabs
            v-model="activeName"
            @tab-click="handleClick"
            class="eltable-rank"
          >
            <el-tab-pane label="&nbsp;&nbsp;发文" name="first">
              <div class="antical-lists" style="height: 850px; overflow: auto">
                <div
                  v-for="data in articleData"
                  :key="data.rank"
                  class="article-item"
                >
                  <p
                    class="rank"
                    :class="{ red: data.rank <= 3, bold: data.rank <= 3 }"
                  >
                    {{ data.rank }}
                  </p>
                  <img
                    :src="data.picture"
                    alt="Avatar"
                    class="avatar"
                    :class="{ 'green-border': data.rank <= 3 }"
                  />
                  <p class="name" :class="{ bold: data.rank <= 3 }">
                    {{ data.name }}
                  </p>
                  <p class="number" :class="{ bold: data.rank <= 3 }">
                    {{ data.count }}
                  </p>
                  <span v-if="data.rank <= 3" class="crown"></span>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="&nbsp;&nbsp;点赞" name="second">
              <div class="like-lists" style="height: 850px; overflow: auto">
                <div
                  v-for="data in postData"
                  :key="data.rank"
                  class="article-item"
                >
                  <p
                    class="rank"
                    :class="{ red: data.rank <= 3, bold: data.rank <= 3 }"
                  >
                    {{ data.rank }}
                  </p>
                  <img
                    :src="data.picture"
                    alt="Avatar"
                    class="avatar"
                    :class="{ 'green-border': data.rank <= 3 }"
                  />
                  <p class="name" :class="{ bold: data.rank <= 3 }">
                    {{ data.name }}
                  </p>
                  <p class="number" :class="{ bold: data.rank <= 3 }">
                    {{ data.count }}
                  </p>
                  <span v-if="data.rank <= 3" class="crown"></span>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </div>
  </div>
  <el-dialog
    v-model="dialogCommentVisible"
    title="评论"
    width="500px"
    modal="false"
  >
    <el-form>
      <el-form-item>
        <el-input v-model="comment" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogCommentVisible = false">取消</el-button>
        <el-button type="primary" @click="createComment">发布</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import qs from "querystring";
import store from "../../store";

import { inject } from "vue";
const axios = inject("axios");
const route = useRoute();
const router = useRouter();
const uid = route.params.uid;
const gid = route.params.gid;
const isadmin = route.params.is_admin;
const dialogCommentVisible = ref(false);
const commentaid = ref();
const comment = ref();
const imageurls = ref([]);
//文章
const articalData = ref([]);
//点赞文章
const isliked = ref([]);

async function sendLikeMessage(aid) {
  try {
    var myDate = new Date();
    const response = await axios.post(
      "/likeArtical/",
      qs.stringify({
        uid: uid,
        aid: aid,
        currentime: myDate.toLocaleString(),
      })
    );
    if (response.data.state == 1) {
      alert(response.data.msg);
    } else {
      alert(response.data.msg);
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

async function sendUnlikeMessage(aid) {
  try {
    const response = await axios.delete("/likeArtical/", {
      params: {
        uid: uid,
        aid: aid,
      },
    });
    if (response.data.state == 1) {
      alert(response.data.msg);
    } else {
      alert(response.data.msg);
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

function isLiked_user() {
  const length = articalData.value.length;
  isliked.value = Array.from({ length }, () => false);
  for (let i = 0; i < articalData.value.length; i++) {
    let likelist = [];
    likelist = articalData.value[i].likeList;

    for (let j = 0; j < likelist.length; j++) {
      if (likelist[j].uid == uid) {
        isliked.value[i] = true;
      }
    }
  }
  console.log(isliked.value);
}

async function likeArticalClick(aid, index) {
  let temp = isliked.value[index];
  isliked.value[index] = !temp;
  if (isliked.value[index]) {
    // 发送点赞消息
    sendLikeMessage(aid);
    const articalRes = await axios.get("/loadArctial/", {
      params: { gid: gid },
    });
    articalData.value = articalRes.data;
    console.log("666");
    isLiked_user();
    isCollected_user();
  } else {
    // 发送取消点赞消息
    sendUnlikeMessage(aid);
    const articalRes = await axios.get("/loadArctial/", {
      params: { gid: gid },
    });
    articalData.value = articalRes.data;
    console.log("liked:");
    isLiked_user();
    isCollected_user();
  }
}

//收藏文章
const iscollected = ref([]);

async function sendcollectMessage(aid) {
  try {
    var myDate = new Date();
    const response = await axios.post(
      "/collectArtical/",
      qs.stringify({
        uid: uid,
        aid: aid,
        currentime: myDate.toLocaleString(),
      })
    );
    window.location.reload();
    if (response.data.state == 1) {
      alert(response.data.msg);
    } else {
      alert(response.data.msg);
    }
  } catch (error) {
    alert(error);
  }
}

async function sendUncollectMessage(aid) {
  try {
    var myDate = new Date();
    const response = await axios.delete("/collectArtical/", {
      params: {
        uid: uid,
        aid: aid,
      },
    });
    window.location.reload();
    if (response.data.state == 1) {
      alert(response.data.msg);
    } else {
      alert(response.data.msg);
    }
  } catch (error) {
    alert(error);
  }
}
function isCollected_user() {
  const length = articalData.value.length;
  iscollected.value = Array.from({ length }, () => false);
  for (let i = 0; i < articalData.value.length; i++) {
    let collectlist = [];
    collectlist = articalData.value[i].favoritesList;

    for (let j = 0; j < collectlist.length; j++) {
      if (collectlist[j].uid == uid) {
        iscollected.value[i] = true;
      }
    }
  }
  console.log(iscollected.value);
}

async function collectArticalClick(aid, index) {
  let temp = iscollected.value[index];
  iscollected.value[index] = !temp;
  if (iscollected.value[index]) {
    sendcollectMessage(aid);
    const articalRes = await axios.get("/loadArctial/", {
      params: { gid: gid },
    });
    articalData.value = articalRes.data;
    isLiked_user();
    isCollected_user();
  } else {
    sendUncollectMessage(aid);
    const articalRes = await axios.get("/loadArctial/", {
      params: { gid: gid },
    });
    articalData.value = articalRes.data;
    isLiked_user();
    isCollected_user();
  }
}

//评论文章
async function createComment() {
  try {
    var myDate = new Date();
    const response = await axios.post(
      "/commentArtical/",
      qs.stringify({
        uid: uid,
        aid: commentaid.value,
        comment: comment.value,
        currentime: myDate.toLocaleString(),
      })
    );
    if (response.data.state == 1) {
      alert(response.data.msg);
      const articalRes = await axios.get("/loadArctial/", {
        params: { gid: gid },
      });
      articalData.value = articalRes.data;
      isLiked_user();
      isCollected_user();
      dialogCommentVisible.value = false;
    } else {
      alert(response.data.msg);
    }
  } catch (error) {
    alert(error);
  }
}
function commentArticalClick(aid) {
  dialogCommentVisible.value = true;
  commentaid.value = aid;
}

//管理员删除文章
async function deleteArticalClick(aid) {
  try {
    const confirmed = confirm("是否要删除文章？");
    if (confirmed) {
      console.log(aid);
      const response = await axios.delete("/ArticalDetail/", {
        params: {
          aid: aid,
        },
      });
      if (response.data.state == 1) {
        alert(response.data.msg);
        const articalRes = await axios.get("/loadArctial/", {
          params: { gid: gid },
        });
        articalData.value = articalRes.data;
      } else {
        alert(response.data.msg);
      }
      window.location.reload();
    }
  } catch (error) {
    alert(error);
  }
}

//用户自己删除文章
async function deleteownArticalClick(aid) {
  try {
    const confirmed = confirm("是否要删除文章？");
    if (confirmed) {
      console.log(aid);
      const response = await axios.delete("/ArticalDetail/", {
        params: {
          aid: aid,
        },
      });
      if (response.data.state == 1) {
        alert(response.data.msg);
        const articalRes = await axios.get("/loadArctial/", {
          params: { gid: gid },
        });
        articalData.value = articalRes.data;
      } else {
        alert(response.data.msg);
      }
      window.location.reload();
    }
  } catch (error) {
    alert(error);
  }
}

//用户自己修改文章
function editArticalClick(aid) {
  router.push(`/${uid}/updatepost/${aid}`);
}

//小组侧边栏
const groupData = ref();

//排行榜
const activeName = ref("first");
const activeIndex = ref(0);
const articleData = ref([]);
const postData = ref([]);

const handleClick = () => {
  activeIndex.value = activeName.value === "first" ? 0 : 1;
};

function gotoHomePage() {
  router.push(`/${uid}`);
}

onMounted(() => {
  try {
    console.log("store", store.state.isLogin);
    axios.get("/rankArtical/", { params: { gid: gid } }).then((articleRes) => {
      articleData.value = articleRes.data;
      console.log(articleRes);
    });

    axios.get("/rankLike/", { params: { gid: gid } }).then((postRes) => {
      postData.value = postRes.data;
      console.log(postRes);
    });

    axios
      .get("/User_GroupDetail/", { params: { gid: gid } })
      .then((groupRes) => {
        groupData.value = groupRes.data[0].group_name;
        console.log(groupData.value);
      });

    axios.get("/loadArctial/", { params: { gid: gid } }).then((articalsRes) => {
      articalData.value = articalsRes.data;
      console.log(articalData.value);
      let length = articalData.value.length;
      imageurls.value = Array.from({ length }, () => []);
      // for(let i=0;i<articalData.value.length;i++){
      //   if(articalData.value[i].imageurl != null){
      //     imageurls.value[i] = articalData.value[i].imageurl.trim().split(' ')
      //   }
      // }
      for (let i = 0; i < length; i++) {
        const url = articalData.value[i].imageurl;
        if (url) {
          imageurls.value[i] = url.trim().split(" ");
        } else {
          imageurls.value[i] = [];
        }
      }
      console.log(imageurls);
      isLiked_user();
      isCollected_user();
    });
  } catch (error) {
    // 错误处理
    console.error("An error occurred:", error);
  }
});
</script>

<style lang="scss" scoped>
.friendcircle-content {
  margin-top: 70px;
  .user-banner {
    //font-size: 20px;
    margin-left: 45px;
    color: #9ba7b9;
  }
  .main-list {
    display: flex;
    justify-content: space-between;

    /* 左边栏样式 */
    .group-list {
      box-shadow: 2px 0px 3px 0px #ddd;
      flex-basis: 15%;
      background-color: #fcfcfe;
      margin-right: 5px;
      height: 1000px;
      .group-message {
        margin-top: 10px;
        display: flex;
        align-items: center;
        background-color: rgb(67, 166, 227);
        color: white;
        font-weight: bold;
        padding: 0px;
      }
      .avatar {
        margin-right: 10px;
      }
    }

    /* 文章样式 */
    .artical-list {
      flex-basis: 60%;
      background-color: #fcfcfe;
      box-shadow: 2px 2px 5px 0px #ddd;
      margin: 0 10px;
      height: 1000px;
      .post-lists {
        height: 1000px;
        overflow: auto;
      }

      .post-item {
        background-color: #f6f6f9;
        padding: 10px;
        margin-bottom: 15px;
      }

      .post-content {
        display: flex;
        align-items: center;
      }

      .image {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        object-fit: cover;
        margin-right: 10px;
      }

      .user-name {
        font-weight: bold;
        max-width: 200px;
      }

      .content {
        margin-top: 5px;
        margin-left: 60px;
        margin-right: 10px;
        letter-spacing: 0.1em;
        line-height: 1.5;
      }
      .content-image {
        display: flex;
        flex-wrap: wrap;
      }

      .image-wrapper {
        flex-basis: 33%; /* 每个图片占据一半宽度 */
        box-sizing: border-box; /* 包含padding和border在内的尺寸计算方式 */
        padding: 0px; /* 图片之间的间距 */
      }

      .icon-time-style {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-right: 10px;
        margin-left: 10px;
      }

      .atime {
        color: gray;
        margin-right: 10px;
      }

      .icons {
        margin-left: auto;
      }
      .icons > * {
        margin-right: 8px;
      }

      .like-list {
        margin-top: 10px;
      }

      .comment-list {
        margin-top: 10px;
        margin-right: 10px;
        display: flex;
        flex-direction: column; /* 纵向排列 */
      }

      .comment-list > div {
        display: flex; /* 横向排列 */
        //align-items: center; /* 垂直居中对齐 */
        margin-bottom: 10px; /* 添加一些间距 */
      }

      .commenter {
        margin-right: 10px; /* 评论者和评论之间添加一些间距 */
      }

      .comment {
        flex: 1; /* 占据剩余空间 */
      }

      .divider {
        border: none;
        border-top: 1px solid rgb(243, 218, 183);
        //margin: 10px 0;
        width: 80%;
        margin-top: 5px;
      }
    }

    /* 排行榜样式 */
    .ranking-list {
      box-shadow: 0 2px 6px 0 #ddd;
      flex-basis: 25%;
      background-color: #fcfcfe; /* 设置背景颜色为蓝色 */
      margin-left: 5px; /* 设置左侧间距为 10px */
      margin-right: 10px;
      height: 1000px;
      .title-rank {
        height: 75px;
        .rank0-img {
          margin-top: 5px;
          width: 160px;
          height: 80px;
          margin-left: 150px;
        }
      }
      .article-item {
        display: flex;
        align-items: center;
        margin-top: 18px;
        margin-bottom: 30px;
        margin-left: 15px;
        position: relative;
      }
      .rank {
        color: black;
        margin-right: 10px;
      }
      .red {
        color: red;
      }
      .avatar {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        margin-right: 10px;
        border: 2px solid transparent;
      }
      .green-border {
        border-color: rgb(235, 177, 42);
      }
      .crown {
        content: "";
        position: absolute;
        top: -18px;
        left: -10px;
        width: 30px;
        height: 30px;
        margin-left: 39px;
        background-image: url("../../assets/crown.png"); /* 替换为您自己的王冠图标路径 */
        background-size: cover;
      }
      .name {
        flex-grow: 1;
        font-weight: normal;
      }
      .bold {
        font-weight: bold;
      }
      .number {
        margin-left: auto;
        margin-right: 30px;
      }
    }
  }
}
</style>
