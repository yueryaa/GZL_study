<template>
  <el-header height="44px" />
  <el-container>
    <!-- 我的小组侧边栏 -->
    <el-aside class="left">
      <p class="title">我的小组</p>
      <el-scrollbar class="list">
        <el-table
          :data="groups"
          :show-header="false"
          class="table"
          v-if="groups.length > 0"
          @row-click="gotoFriendCircle"
        >
          <el-table-column width="6" />
          <el-table-column width="62">
            <img src="../assets/group.png" class="avatar" />
          </el-table-column>
          <el-table-column width="6" />
          <el-table-column
            prop="group_name"
            width="235"
            show-overflow-tooltip="true"
          />
          <el-table-column width="90">
            <template #default="scope">
              <el-button
                type="primary"
                v-if="scope.row.is_admin === 1"
                @click.stop="admin(scope.row.gid)"
                >管理</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-scrollbar>
      <div class="bottom">
        <span>
          <el-button type="primary" @click="clickCreate">创建小组</el-button>
        </span>
        <span style="padding-left: 50px">
          <el-button type="primary" @click="clickJoin">加入小组</el-button>
        </span>
      </div>
    </el-aside>

    <!-- 通知栏 -->
    <el-container>
      <el-aside width="200px" />
      <el-main>
        <el-header height="20px" />
        <el-card
          class="box-card"
          body-style="padding: 10px; padding-left: 20px; padding-right: 40px;"
        >
          <template #header>
            <div class="card-header">管理员通知</div>
          </template>
          <el-scrollbar class="info-list">
            <el-table
              :data="showJoinInfo"
              :show-header="false"
              v-if="showJoinInfo.length > 0"
            >
              <el-table-column width="660">
                <template #default="scope">
                  <p>{{ scope.row.p1 }}</p>
                  <p>{{ scope.row.p2 }}</p>
                </template>
              </el-table-column>
              <el-table-column width="25" />
              <el-table-column width="88">
                <template #default="scope">
                  <el-button type="primary" @click="accept(scope.$index)"
                    >同意</el-button
                  >
                </template>
              </el-table-column>
              <el-table-column width="88">
                <template #default="scope">
                  <el-button @click="refuse(scope.$index)">拒绝</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-scrollbar>
        </el-card>
        <div style="height: 22px"></div>
        <el-card
          class="box-card"
          body-style="padding: 10px; padding-left: 20px; padding-right: 40px;"
        >
          <template #header>
            <div class="card-header">互动通知</div>
          </template>
          <el-scrollbar class="info-list">
            <el-table
              :data="showInteractionInfo"
              :show-header="false"
              v-if="showInteractionInfo.length > 0"
            >
              <el-table-column width="750">
                <template #default="scope">{{ scope.row }}</template>
              </el-table-column>
              <el-table-column width="30" />
              <el-table-column width="81">
                <template #default="scope">
                  <el-button
                    :icon="CloseBold"
                    text
                    @click="deleteInfo(scope.$index)"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-scrollbar>
        </el-card>
      </el-main>
    </el-container>
  </el-container>

  <!-- 管理成员对话框 -->
  <el-dialog
    v-model="dialogAdminVisible"
    :title="'管理小组成员（组号：' + adminGid + '）'"
    width="650px"
  >
    <el-table :data="members" max-height="405px">
      <el-table-column
        prop="User_name"
        label="成员列表"
        width="400"
        align="center"
        show-overflow-tooltip="true"
      />
      <el-table-column width="200" label="操作" align="center">
        <template #default="scope">
          <el-button type="primary" @click="deleteMember(scope.$index)"
            >移除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>

  <!-- 创建小组对话框 -->
  <el-dialog v-model="dialogCreateVisible" title="创建小组" width="500px">
    <el-form :model="form1">
      <el-form-item label="请输入组名">
        <el-input v-model="form1.name" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogCreateVisible = false">取消</el-button>
        <el-button type="primary" @click="createGroup">创建</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 加入小组对话框 -->
  <el-dialog v-model="dialogJoinVisible" title="加入小组" width="500px">
    <el-form :model="form2">
      <el-form-item label="请输入组号">
        <el-input v-model="form2.gid" autocomplete="off" />
      </el-form-item>
      <el-form-item label="请输入验证信息">
        <el-input v-model="form2.msg" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogJoinVisible = false">取消</el-button>
        <el-button type="primary" @click="joinGroup">提交</el-button>
      </span>
    </template>
  </el-dialog>
</template>
  
<script setup>
import { ref, reactive, inject, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import qs from "querystring";
import { ElMessage, ElMessageBox } from "element-plus";
import { CloseBold } from "@element-plus/icons-vue";

const axios = inject("axios");
const router = useRouter();
const route = useRoute();
const uid = route.params.uid;
const adminGid = ref();

const dialogAdminVisible = ref(false);
const dialogCreateVisible = ref(false);
const dialogJoinVisible = ref(false);

/* 小组列表 */
const groups = reactive([]);
/* 小组成员列表 */
const members = reactive([]);
/* 创建小组的表单 */
const form1 = reactive({
  name: "",
});
/* 加入小组的表单 */
const form2 = reactive({
  gid: "",
  msg: "",
});
/* 管理员通知的原始数据 */
const joinInfo = reactive([]);
/* 管理员通知的显示数据 */
const showJoinInfo = reactive([]);
/* 互动通知的原始数据 */
const interactionInfo = reactive([]);
/* 互动通知的显示数据 */
const showInteractionInfo = reactive([]);

onMounted(() => {
  /* 获取小组列表 */
  axios.get("/user_group/", { params: { id: uid } }).then((res) => {
    groups.splice(0, groups.length, ...res.data);
  });
  /* 获取管理员通知 */
  axios.get("/ApplicationDetail/", { params: { id: uid } }).then((res) => {
    joinInfo.splice(0, joinInfo.length, ...res.data);
    console.log(res.data);
    for (var i = 0; i < joinInfo.length; i++) {
      var str1 = joinInfo[i].User_name + " 申请加入 " + joinInfo[i].group_name;
      var str2 = "验证信息： " + joinInfo[i].msg;
      showJoinInfo.push({ p1: str1, p2: str2 });
    }
  });
  /* 获取互动通知 */
  axios.get("/interaction_info/", { params: { id: uid } }).then((res) => {
    let sepDot = '\xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0  \xa0 \xa0 \xa0 \xa0 \xa0  \xa0';
    interactionInfo.splice(0, interactionInfo.length, ...res.data);
    for (var i = 0; i < interactionInfo.length; i++) {
      var str =
        interactionInfo[i].name +
        " " +
        interactionInfo[i].ncontent +
        "了你的文章"+sepDot+sepDot+sepDot+interactionInfo[i].ntime;
      showInteractionInfo.push(str);
    }
  });
});

/* 跳转到学习圈 */
function gotoFriendCircle(row) {
  router.push(`/${uid}/${row.gid}/${row.is_admin}`);
}

/* 显示小组成员 */
function admin(gid) {
  adminGid.value = gid;
  axios.get("/User_GroupDetail/", { params: { gid: gid } }).then((res) => {
    members.splice(0, members.length, ...res.data);
    dialogAdminVisible.value = true;
  });
}

/* 删除小组成员 */
function deleteMember(index) {
  ElMessageBox.confirm("确定要删除该成员吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
  })
    .then(() => {
      axios
        .delete("/User_GroupDetail/", {
          params: { id: members[index].uid, gid: members[index].gid },
        })
        .then((res) => {
          if (res.data.msg == "删除成功") {
            /* 更新小组成员列表 */
            members.splice(index, 1);
            ElMessage({
              message: "删除成功",
              type: "success",
            });
          } else {
            ElMessage.error("删除失败");
          }
        });
    })
    .catch(() => {});
}

/* 点击创建小组 */
function clickCreate() {
  /* 清空表单 */
  Object.keys(form1).forEach((key) => (form1[key] = ""));
  dialogCreateVisible.value = true;
}

/* 点击加入小组 */
function clickJoin() {
  /* 清空表单 */
  Object.keys(form2).forEach((key) => (form2[key] = ""));
  dialogJoinVisible.value = true;
}

/* 创建小组 */
function createGroup() {
  axios
    .post("/creat_group/", qs.stringify({ uid: uid, name: form1.name }))
    .then((res) => {
      /* 更新小组列表 */
      axios.get("/user_group/", { params: { id: uid } }).then((res) => {
        groups.splice(0, groups.length, ...res.data);
      });
      dialogCreateVisible.value = false;
      ElMessageBox.alert(
        `小组创建成功！ 组号为 ${res.data.gid} ，组名为 ${res.data.name} `,
        "提示",
        {
          confirmButtonText: "OK",
        }
      );
    });
}

/* 加入小组 */
function joinGroup() {
  axios
    .post(
      "/ApplicationDetail/",
      qs.stringify({ id: uid, gid: form2.gid, msg: form2.msg })
    )
    .then((res) => {
      if (res.data.msg == "成功发送申请") {
        dialogJoinVisible.value = false;
        ElMessageBox.alert("申请成功提交，等待管理员审核", "提示", {
          confirmButtonText: "OK",
        });
      } else if (res.data.msg == "不存在该小组") {
        ElMessageBox.alert("输入的组号不存在，请重新输入", "提示", {
          confirmButtonText: "OK",
        });
      } else if (res.data.msg == "您已在该小组内") {
        ElMessageBox.alert("您已是该小组成员，申请无效", "提示", {
          confirmButtonText: "OK",
        });
      } else if (res.data.msg == "重复发送申请，请耐心等待") {
        ElMessageBox.alert("存在重复申请，请耐心等待", "提示", {
          confirmButtonText: "OK",
        });
      } else {
      }
    });
}

/* 同意加入小组 */
function accept(index) {
  ElMessageBox.confirm(
    `确定要同意 ${joinInfo[index].User_name} 加入小组吗？`,
    "提示",
    { confirmButtonText: "确定", cancelButtonText: "取消" }
  )
    .then(() => {
      axios
        .delete("/ApplicationDetail/", {
          params: {
            id: joinInfo[index].uid,
            gid: joinInfo[index].gid,
            state: 1,
          },
        })
        .then((res) => {
          console.log(res.data);
          if (res.data.msg == "同意申请成功") {
            /* 更新管理员通知 */
            joinInfo.splice(index, 1);
            showJoinInfo.splice(index, 1);
            ElMessage({
              message: "同意申请成功",
              type: "success",
            });
          } else {
            ElMessage.error("操作失败");
          }
        });
    })
    .catch(() => {});
}

/* 拒绝加入小组 */
function refuse(index) {
  ElMessageBox.confirm(
    `确定要拒绝 ${joinInfo[index].User_name} 加入小组吗？`,
    "提示",
    { confirmButtonText: "确定", cancelButtonText: "取消" }
  )
    .then(() => {
      axios
        .delete("/ApplicationDetail/", {
          params: {
            id: joinInfo[index].uid,
            gid: joinInfo[index].gid,
            state: 0,
          },
        })
        .then((res) => {
          if (res.data.msg == "拒绝申请成功") {
            /* 更新管理员通知 */
            joinInfo.splice(index, 1);
            showJoinInfo.splice(index, 1);
            ElMessage({
              message: "拒绝申请成功",
              type: "success",
            });
          } else {
            ElMessage.error("操作失败");
          }
        });
    })
    .catch(() => {});
}

/* 删除互动通知 */
function deleteInfo(index) {
  axios
    .delete("/interaction_info/", {
      params: { nid: interactionInfo[index].nid },
    })
    .then((res) => {
      if (res.data.msg == "删除成功") {
        /* 更新互动通知 */
        interactionInfo.splice(index, 1);
        showInteractionInfo.splice(index, 1);
      }
    });
}
</script>

<style scoped>
.tab {
    display: inline-block;
    width: 4em; /* 调整此处的数值可以控制空格的宽度 */
}
.left {
  width: 400px;
  border-right: 1.2px solid rgb(200, 200, 200);
  background-color: rgb(245, 245, 245);
}

.title {
  font-size: 18px;
  height: 40px;
  padding: 18px;
  padding-left: 160px;
  color: black;
}

.list {
  height: 745px;
  border-top: 1.2px solid rgb(200, 200, 200);
  border-bottom: 1.2px solid rgb(200, 200, 200);
}

.table {
  font-size: 14.5px;
  color: black;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 5px;
}

.bottom {
  height: 66px;
  padding: 18px;
  padding-left: 85px;
}

.box-card {
  width: 950px;
  height: 400px;
}

.card-header {
  padding-left: 5px;
  color: black;
}

.info-list {
  height: 310px;
  padding-left: 20px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>