<template>
  <div style="height: 72px"></div>
  <div class="user-banner">
    <a @click="gotoHomePage" style="color: #3285ff">首页</a>
    <span>&nbsp;&nbsp;>&nbsp;&nbsp;修改文章</span>
  </div>
  <div style="height: 3px"></div>

  <el-form
    :model="form"
    :rules="rules"
    ref="formRef"
    label-width="300px"
    style="width: 1200px"
  >
    <el-form-item label="小组" prop="gid">
      <el-select v-model="form.gid" placeholder="请选择小组">
        <el-option
          v-for="item in groups"
          :label="item.group_name"
          :value="item.gid"
          :key="item.gid"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="内容" prop="content">
      <el-input v-model="form.content" :rows="15" type="textarea" />
    </el-form-item>

    <el-form-item label="图片">
      <el-upload
        v-model:file-list="fileList"
        action=""
        list-type="picture-card"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :auto-upload="false"
      >
        <el-icon>
          <Plus />
        </el-icon>
      </el-upload>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submit">提交修改</el-button>
      <el-button @click="cancel">取消</el-button>
    </el-form-item>
  </el-form>

  <el-dialog v-model="dialogVisible" title="图片预览">
    <img w-full :src="dialogImageurl" alt="Preview Image" />
  </el-dialog>
</template>
  
<script setup>
import { ref, reactive, inject, onBeforeMount } from "vue";
import { useRouter, useRoute } from "vue-router";
import qs from "querystring";
import { ElMessage } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import { client } from "../utils/alioss.js";

const axios = inject("axios");
const router = useRouter();
const route = useRoute();
const uid = route.params.uid;
const aid = route.params.aid;
const groups = reactive([]);
const form = reactive({
  aid: "",
  uid: "",
  gid: "",
  content: "",
  imageurl: "",
  atime: "",
});
const rules = reactive({
  gid: [{ required: true, message: "请选择小组" }],
  content: [{ required: true, message: "请输入内容" }],
});
const formRef = ref();
const fileList = reactive([]);
const fileName = reactive([]);
const dialogImageurl = ref("");
const dialogVisible = ref(false);

onBeforeMount(() => {
  /* 获取修改前的文章信息 */
  axios.get("/ArticalDetail/", { params: { aid: aid } }).then((res) => {
    Object.keys(form).forEach((key) => {
      form[key] = res.data[key];
    });
    if (form.imageurl) {
      var imgurl = form.imageurl.split(" "); //将imageurl从字符串转换为数组
      for (var i = 0; i < imgurl.length; i++) {
        fileList.push({ url: imgurl[i] });
      }
    }
  });
  /* 获取小组列表 */
  axios.get("/user_group/", { params: { id: uid } }).then((res) => {
    groups.splice(0, groups.length, ...res.data);
  });
});

function handlePreview(file) {
  dialogImageurl.value = file.url;
  dialogVisible.value = true;
}

function handleRemove(file, files) {
  fileList.splice(0, fileList.length, ...files);
}

function handleChange(file, files) {
  fileList.splice(0, fileList.length, ...files);
}

function submit() {
  /* 给imageurl数组赋值 */
  form.imageurl = "";
  fileName.splice(0, fileName.length);
  for (var i = 0; i < fileList.length; i++) {
    //原有的图片
    if (fileList[i].raw == undefined) {
      fileName.push("");
      form.imageurl = form.imageurl + " " + fileList[i].url;
    }
    //新增的图片
    else {
      fileName.push(`${Date.parse(new Date())}` + `${i}`);
      form.imageurl =
        form.imageurl +
        " http://userp.oss-cn-beijing.aliyuncs.com/" +
        fileName[i];
    }
  }
  form.imageurl = form.imageurl.trim();
  /* 上传图片到阿里云 */
  for (var i = 0; i < fileList.length; i++) {
    if (fileList[i].raw != undefined) {
      client().multipartUpload(fileName[i], fileList[i].raw);
    }
  }
  /* 必填项不为空才能提交 */
  formRef.value.validate((valid) => {
    if (valid) {
      axios.put("/ArticalDetail/", qs.stringify(form)).then((res) => {
        if (res.data.msg == "修改成功") {
          ElMessage({
            message: "修改成功！快去查看一下吧！",
            type: "success",
          });
          router.push(`/${uid}`);
        }
      });
    }
  });
}

function cancel() {
  router.push(`/${uid}`);
}

function gotoHomePage() {
  router.push(`/${uid}`);
}
</script>

<style scoped>
.user-banner {
  margin-left: 45px;
  color: #9ba7b9;
}
</style>