<template>
  <div class="post-lists">
    <div class="post-content">
      <img :src="data.picture" alt="image" class="image" />
      <div class="user-info">
        <div class="user-name">{{ data.name }}</div>
      </div>
      <div v-if="data.uid == uid">
        <el-dropdown :style="{ 'margin-left': '1250px' }">
          <span class="el-dropdown-link">
            <el-icon><MoreFilled /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="deleteownArticalClick(data.aid)"
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
    <div
      class="content"
      @mouseenter="showIcons = true"
      @mouseleave="showIcons = false"
    >
      {{ data.content }}
      <div class="content-image">
        <div
          v-for="(img, index) in imageList"
          :key="index"
          class="image-wrapper"
        >
          <el-image
            style="width: 300px; height: 200px"
            :src="img"
            fit="cover"
            @error="handleError"
            :preview-src-list="imageList"
          >
            <template #error>
              <div class="image-slot">
                <el-icon name="el-icon-picture" />
              </div>
            </template>
          </el-image>
        </div>
      </div>
    </div>
    <div class="icon-time-style">
      <div class="atime">{{ data.atime }}</div>
      <div class="icons">
        <span
          v-if="liked"
          class="iconfont icon-good"
          :style="{ color: '#f05b72', 'font-size': '20px' }"
          @click="likeArticalClick(data.aid)"
        ></span>
        <span
          v-else
          class="iconfont icon-like"
          :style="{ color: '#f05b72', 'font-size': '20px' }"
          @click="likeArticalClick(data.aid)"
        ></span>

        <span
          v-if="collected"
          class="iconfont icon-user-filling"
          :style="{ color: '#FFBA02' }"
          @click="collectArticalClick(data.aid)"
        ></span>
        <span
          v-else
          class="iconfont icon-empty"
          :style="{ color: '#FFBA02' }"
          @click="collectArticalClick(data.aid)"
        ></span>

        <span
          class="iconfont icon-comment"
          :style="{ color: '#78a355' }"
          @click="commentArticalClick(data.aid)"
        ></span>
      </div>
    </div>
    <div class="like-list" v-show="showIcons">
      <span
        class="iconfont icon-good"
        :style="{ color: '#f05b72' }"
        v-if="data.likeList.length > 0"
      ></span>
      {{ data.likeList.map((item) => item.name).join(", ") }}
    </div>
    <div class="comment-list" v-show="showIcons">
      <div v-for="(comment, cIndex) in data.commentList" :key="cIndex">
        <div class="commenter">
          <el-icon color="#78a355"><UserFilled /></el-icon> {{ comment.name }}:
        </div>
        <div class="comment">{{ comment.content }}</div>
      </div>
    </div>
    <hr class="divider" />
  </div>
  <el-dialog
    v-model="dialogCommentVisible"
    title="评论"
    width="500px"
    modal="false"
  >
    <el-form>
      <el-form-item
        ><el-input v-model="comment" autocomplete="off"
      /></el-form-item>
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
import { ref, getCurrentInstance, defineEmits, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import qs from "querystring";
import { inject } from "vue";
import { onMounted } from "vue";

const axios = inject("axios");
const commentaid = ref();
const emits = defineEmits([
  "update:ownartical",
  "update:ownlikeartical",
  "update:owncollectartical",
]);
const props = defineProps({
  data: Object,
  gid: String,
  mode: String,
  isliked: Boolean,
  iscollected: Boolean,
});

const route = useRoute();
const router = useRouter();
const uid = route.params.uid;
const dialogCommentVisible = ref(false);
const comment = ref();
const showIcons = ref(false);
const imageList = ref([]);

function getImagelist() {
  let url = props.data.imageurl;
  if (url) {
    imageList.value = url.trim().split(" ");
  }
}

onMounted(() => {
  getImagelist();
  //isLiked()
});
//文章
const updatedData = ref([]);
//点赞文章
const liked = ref();

function isLiked() {
  let likelist = [];
  likelist = props.data.likeList;
  console.log(props.data.likeList);
  for (let i = 0; i < props.data.length; i++) {
    if (likelist[i].uid == uid) {
      liked.value = true;
    }
  }
  //console.log(uid);
  //console.log(liked);
}

async function sendLikeMessage(aid) {
  try {
    var myDate = new Date();
    const gid = props.gid;
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
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

async function sendUnlikeMessage(aid) {
  try {
    const gid = props.gid;
    const response = await axios.delete("/likeArtical/", {
      params: {
        uid: uid,
        aid: aid,
      },
    });
    if (response.data.state == 1) {
      alert(response.data.msg);
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

async function likeArticalClick(aid) {
  liked.value = !liked.value;
  if (liked.value) {
    // 发送点赞消息
    sendLikeMessage(aid);
  } else {
    // 发送取消点赞消息
    sendUnlikeMessage(aid);
  }
  const mode = props.mode;
  if (mode == "first") {
    const responseartical = await axios.get("/getownArtical/", {
      params: { id: uid },
    });
    //isLiked();
    //isCollected();
    updatedData.value = responseartical.data;
    console.log(responseartical);
    console.log("3", updatedData.value);
    emits("update:ownartical", updatedData.value);
  }
  if (mode == "second") {
    const responseartical = await axios.get("/getownlikeArtical/", {
      params: { id: uid },
    });
    updatedData.value = responseartical.data;
    emits("update:ownlikeartical", updatedData.value);
  }
  if (mode == "third") {
    const responseartical = await axios.get("/getowncollectArtical/", {
      params: { id: uid },
    });
    updatedData.value = responseartical.data;
    emits("update:owncollectartical", updatedData.value);
  }
}

//收藏文章
const collected = ref(false);
function isCollected() {
  let collectlist = [];
  collectlist = data.favoritesList;
  for (let i = 0; i < collect.length; i++) {
    if (collectlist[i].uid == uid) {
      collected.value = true;
    }
  }
}

async function sendcollectMessage(aid) {
  try {
    var myDate = new Date();
    const gid = props.gid;
    const response = await axios.post(
      "/collectArtical/",
      qs.stringify({
        uid: uid,
        aid: aid,
        currentime: myDate.toLocaleString(),
      })
    );
    if (response.data.state == 1) {
      alert(response.data.msg);
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

async function sendUncollectMessage(aid) {
  try {
    var myDate = new Date();
    const gid = props.gid;
    const response = await axios.delete("/collectArtical/", {
      params: {
        uid: uid,
        aid: aid,
      },
    });
    if (response.data.status == 1) {
      alert(response.data.msg);
    }
    window.location.reload();
  } catch (error) {
    alert(error);
  }
}

async function collectArticalClick(aid) {
  collected.value = !collected.value;
  if (collected.value) {
    // 发送收藏消息
    sendcollectMessage(aid);
  } else {
    // 发送取消收藏消息
    sendUncollectMessage(aid);
  }
  const mode = props.mode;
  if (mode == "first") {
    const responseartical = await axios.get("/getownArtical/", {
      params: { id: uid },
    });
    updatedData.value = responseartical.data;
    emits("update:ownartical", updatedData.value);
  }
  if (mode == "second") {
    const responseartical = await axios.get("/getownlikeArtical/", {
      params: { id: uid },
    });
    updatedData.value = responseartical.data;
    emits("update:ownlikeartical", updatedData.value);
  }
  if (mode == "third") {
    const responseartical = await axios.get("/getowncollectArtical/", {
      params: { id: uid },
    });
    updatedData.value = responseartical.data;
    emits("update:owncollectartical", updatedData.value);
  }
}

//评论文章
async function createComment() {
  try {
    var myDate = new Date();
    const gid = props.gid;
    const mode = props.mode;
    const response = await axios.post(
      "/commentArtical/",
      qs.stringify({
        uid: uid,
        aid: commentaid.value,
        comment: comment.value,
        currentime: myDate.toLocaleString(),
      })
    );
    console.log(response);
    if (response.data.state == 1) {
      alert(response.data.msg);
      dialogCommentVisible.value = false;
      if (mode == "first") {
        const responseartical = await axios.get("/getownArtical/", {
          params: { id: uid },
        });
        updatedData.value = responseartical.data;
        emits("update:ownartical", updatedData.value);
      }
      if (mode == "second") {
        const responseartical = await axios.get("/getownlikeArtical/", {
          params: { id: uid },
        });
        updatedData.value = responseartical.data;
        emits("update:ownlikeartical", updatedData.value);
      }
      if (mode == "third") {
        const responseartical = await axios.get("/getowncollectArtical/", {
          params: { id: uid },
        });
        updatedData.value = responseartical.data;
        emits("update:owncollectartical", updatedData.value);
      }
    }
  } catch (error) {
    alert(error);
  }
}
function commentArticalClick(aid) {
  dialogCommentVisible.value = true;
  commentaid.value = aid;
}

//用户自己删除文章
async function deleteownArticalClick(aid) {
  try {
    const confirmed = confirm("是否要删除文章？");
    if (confirmed) {
      const response = await axios.delete("/ArticalDetail/", {
        params: {
          uid: uid,
          aid: aid,
        },
      });
      if (response.data.state == 1) {
        alert(response.data.msg);
        const mode = props.mode;
        if (mode == "first") {
          const responseartical = await axios.get("/getownArtical/", {
            params: { id: uid },
          });
          updatedData.value = responseartical.data;
          emits("update:ownartical", updatedData.value);
        }
        if (mode == "second") {
          const responseartical = await axios.get("/getownlikeArtical/", {
            params: { id: uid },
          });
          updatedData.value = responseartical.data;
          emits("update:ownlikeartical", updatedData.value);
        }
        if (mode == "third") {
          const responseartical = await axios.get("/getowncollectArtical/", {
            params: { id: uid },
          });
          updatedData.value = responseartical.data;
          emits("update:owncollectartical", updatedData.value);
        }
      } else {
        alert(response.data.msg);
      }
    }
  } catch (error) {
    alert(error);
  }
}
//用户自己修改文章
function editArticalClick(aid) {
  router.push(`/${uid}/updatepost/${aid}`);
}
</script>

<style lang="scss" scoped>
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
  width: 950px;
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
</style>
