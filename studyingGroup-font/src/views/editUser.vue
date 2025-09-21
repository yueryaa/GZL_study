<template>
  <div class="header-content-edit" :style="{ width: '1300px' }">
    <div class="user-banner">
      <a @click="gotoHomePage" style="color: #3285ff">首页</a>
      <span>&nbsp;&nbsp;>&nbsp;&nbsp;个人信息</span>
    </div>

    <div class="base-user-info">
      <div v-if="userExists">
        <div class="left-img">
          <div class="image-container">
            <!-- 默认显示的圆形图片 -->
            <img :src="imageUrl" class="circle-image" alt="默认图片" />

            <!-- 点击图标触发上传图片的功能 -->
            <input type="file" @change="handleImageUpload" id="image-upload" />
            <label for="image-upload" class="upload-icon">
              <img src="../assets/icon1.png" alt="上传图标" />
            </label>
          </div>
        </div>
        <div class="right-base-info">
          <div>昵称：{{ userInfo.data.name }}</div>
          <div>用户id：{{ userInfo.data.uid }}</div>
          <div>性别：{{ userInfo.data.sex }}</div>
          <div>生日：{{ userInfo.data.birthday }}</div>
        </div>
      </div>
      <div v-else>
        <!-- 当用户不存在时显示的内容 -->
        <p>用户不存在或加载失败。</p>
      </div>
    </div>
    <div class="edit-user-info">
      <div class="title-edit">基础信息</div>
      <el-form
        :model="formData"
        :rules="rules"
        ref="formDataRef"
        class="el-form"
      >
        <el-form-item
          label="生日&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          prop="birthday"
        >
          <el-date-picker
            v-model="formData.birthday"
            type="date"
            placeholder="选择日期"
            size="large"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="修改性别" prop="gender">
          <el-radio-group v-model="formData.sex" size="large">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="初始密码" prop="password1">
          <el-input
            v-model="formData.password1"
            size="large"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item label="修改密码" prop="password2">
          <el-input
            v-model="formData.password2"
            size="large"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item label="再次确认" prop="password3">
          <el-input
            v-model="formData.password3"
            size="large"
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="昵称&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          prop="name"
        >
          <el-input v-model="formData.name" size="large"></el-input>
        </el-form-item>
        <el-form-item
          label="邮箱&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          prop="email"
        >
          <el-input v-model="formData.email" size="large"></el-input>
        </el-form-item>
        <el-form-item label="手机号&nbsp;&nbsp;" prop="account">
          <el-input v-model="formData.account" size="large"></el-input>
        </el-form-item>
        <el-form-item label="个人介绍" prop="remark">
          <!--<el-input v-model="formData.remark" size="large"></el-input>-->
          <el-input
            type="textarea"
            :rows="4"
            v-model="formData.remark"
          ></el-input>
        </el-form-item>
      </el-form>
      <div class="buttons-container">
        <el-row class="el-btn">
          <el-button type="primary" round @click="saveInfo">保存</el-button>
          <el-button type="primary" round @click="resetInfo">重置</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
import { ref, onMounted, reactive, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import qs from "querystring";
import CryptoJS from "crypto-js";
import { inject } from "vue";
import { client } from "../utils/alioss.js";
const axios = inject("axios");
const router = useRouter();
const route = useRoute();
const uid = route.params.uid;
const userInfo = ref({}); // 初始化为空对象，避免 undefined 错误
const userExists = ref(false); // 用于标识用户是否存在
// 默认图片的 URL
const imageUrl = ref("../assets/default-image.jpg");
const secretKey = "ThisIsAStrongAndSecureSecretKey12345";

//回到首页
function gotoHomePage() {
  router.push(`/${uid}`);
}
// 获取用户信息
async function fetchUserInfo(userId) {
  try {
    const response = await axios.get("/UserDetail/", { params: { id: uid } });
    userInfo.value = response;
    userExists.value = true; // 用户存在
    console.log(userInfo.value);
    Object.keys(formData).forEach((key) => {
      formData[key] = response.data[key];
    });
    if (formData.picture == undefined) {
      formData.picture = imageUrl;
    } else {
      imageUrl.value = formData.picture;
    }
    console.log(imageUrl);
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // 如果API返回404错误，意味着用户不存在
      userExists.value = false;
    }
  }
}

// 在组件挂载时调用函数
onMounted(() => {
  console.log(uid);
  if (uid) {
    fetchUserInfo(uid);
  }
});

//组件
const formData = reactive({
  uid: "",
  birthday: "",
  password: "",
  password1: "",
  password2: "",
  password3: "",
  account: "",
  name: "",
  email: "",
  remark: "",
  picture: "",
  sex: "",
});

const formDataRef = ref(null);

const rules = {
  password1: [{ required: false, message: "请输入初始密码", trigger: "blur" }],
  password2: [
    { required: false, message: "请输入修改密码", trigger: "blur" },
    // 当修改账号时，初始密码不能为空的规则
    {
      validator: (rule, value) => {
        if (value && !formData.password1) {
          return Promise.reject("请先输入初始密码");
        }
        return Promise.resolve();
      },
      trigger: "blur",
    },
  ],
  password3: [
    { required: false, message: "请再次确认密码", trigger: "blur" },
    // 再次确认的密码要求和修改的密码保持一致的规则
    {
      validator: (rule, value) => {
        if (value !== formData.password2) {
          return Promise.reject("两次输入的密码不一致");
        }
        return Promise.resolve();
      },
      trigger: "blur",
    },
  ],
  email: [
    { required: false, trigger: "blur" },
    { type: "email", message: "邮箱格式不正确", trigger: "blur" },
  ],
};

// 表单验证方法   validateForm函数可以用于提交表单时进行验证。它调用了formDataRef.value.validate方法，
//该方法将执行所有的验证规则，并根据验证结果执行相应的操作。
//如果验证通过，则可以继续提交表单；如果验证失败，则可以显示错误信息。
const resetInfo = () => {
  // 重置 formData 对象的属性为空
  formData.birthday = "";
  formData.name = "";
  formData.password1 = "";
  formData.password2 = "";
  formData.password3 = "";
  formData.account = "";
  formData.picture = "";
  formData.remark = "";
  formData.email = "";
  formData.sex = "";
};

const saveInfo = () => {
  if (formData.password3 == undefined) {
    if(formData.birthday){
      const usergetInfo = reactive({
      uid: formData.uid,
      password: formData.password,
      birthday: formData.birthday.toLocaleString().split(" ")[0],
      account: formData.account,
      name: formData.name,
      email: formData.email,
      remark: formData.remark,
      picture: formData.picture,
      sex: formData.sex,
    });
    console.log(usergetInfo);
    // 发送 PUT 请求，将数据保存到服务器
    axios
      .put("/UserDetail/", qs.stringify(usergetInfo))
      .then((response) => {
        // 处理响应
        fetchUserInfo(uid);
        alert("保存成功！");
      })
      .catch((error) => {
        alert(error);
      });
    }
    else{
      const usergetInfo = reactive({
      uid: formData.uid,
      password: formData.password,
      birthday: formData.birthday,
      account: formData.account,
      name: formData.name,
      email: formData.email,
      remark: formData.remark,
      picture: formData.picture,
      sex: formData.sex,
    });
    console.log(usergetInfo);
    // 发送 PUT 请求，将数据保存到服务器
    axios
      .put("/UserDetail/", qs.stringify(usergetInfo))
      .then((response) => {
        // 处理响应
        fetchUserInfo(uid);
        alert("保存成功！");
      })
      .catch((error) => {
        alert(error);
      });
    }
  } else {
    const decryptedPassword_user = CryptoJS.AES.decrypt(
      formData.password,
      secretKey
    ).toString(CryptoJS.enc.Utf8);
    if (decryptedPassword_user == formData.password1) {
      const encryptedPassword = CryptoJS.AES.encrypt(
        formData.password3,
        secretKey
      ).toString();
      const usergetInfo = reactive({
        uid: formData.uid,
        birthday: formData.birthday.toString(),
        password: encryptedPassword,
        account: formData.account,
        name: formData.name,
        email: formData.email,
        remark: formData.remark,
        picture: formData.picture,
        sex: formData.sex,
      });
      console.log(usergetInfo);
      // 发送 PUT 请求，将数据保存到服务器
      axios
        .put("/UserDetail/", qs.stringify(usergetInfo))
        .then((response) => {
          // 处理响应
          fetchUserInfo(uid);
          alert("保存成功！");
        })
        .catch((error) => {
          alert(error);
        });
    } else {
      alert("初始密码错误请重新输入！");
    }
  }
};

//图片上传
// 处理图片上传事件
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  const fileName = `${Date.parse(new Date())}`;
  client()
    .multipartUpload(fileName, file)
    .then((result) => {
      imageUrl.value = " http://userp.oss-cn-beijing.aliyuncs.com/" + fileName;
      formData.picture = imageUrl.value;
    });
};
</script>
  
  <style scoped>
.header-content-edit {
  margin-top: 70px;
  margin-left: auto;
  margin-right: auto;
  display: flex; /* 使用 Flexbox 布局 */
  flex-direction: column; /* 子元素以列的形式排列（上下布局） */
  /*align-items: center; /* 子元素在水平方向上居中对齐 */
  width: 1300px; /* 容器宽度设置为 700px */
  background-color: #fff; /* 背景颜色设置为灰色 */
}
.user-banner {
  margin-left: -140px;
  color: #9ba7b9;
}
.base-user-info {
  width: 100%; /* 宽度占满父容器 */
  margin-bottom: 10px; /* 与下方模块的距离设置为 10px */
  height: calc(800px * 0.3); /* 高度为父容器高度的 30% */
  background-color: rgb(243, 242, 242); /* 设置背景颜色以区分模块 */
}

.edit-user-info {
  width: 100%; /* 宽度占满父容器 */
  height: calc(900px * 0.7); /* 高度为父容器高度的 70% */
  background-color: rgb(245, 245, 246); /* 设置背景颜色以区分模块 */
}
.title-edit {
  width: 90px;
  font-weight: bold;
  color: rgb(110, 110, 225);
  background-color: rgb(231, 231, 231);
  border-radius: 20px;
  padding: 10px;
  margin: 10px;
}
.parent-container {
  display: flex;
}

.left-img {
  width: 170px;
  height: 220px;

  margin-top: 30px;
  margin-left: 20px;
  overflow: hidden;
}

.image-container {
  position: relative;
}

.circle-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}

.upload-icon {
  position: absolute;
  bottom: -10px;
  right: 10px;
}

/*隐藏原生的文件上传按钮 */
input[type="file"] {
  display: none;
}
.right-base-info {
  margin-left: 230px;
  font-size: 13px;
  line-height: 3;
  color: #565656;
  margin-top: -220px; /*left-img de hight高度 */
}

.right-base-info > div {
  margin-bottom: 10px;
}
.el-form {
  width: 600px;
  margin-left: 100px;
  /*margin-right: auto;*/
}
.buttons-container {
  margin-top: 20px;
  display: flex; /* 设置flex布局 */
  justify-content: center; /* 水平居中 */
  align-items: center;
  /* 垂直居中（如果需要） */
}
.el-btn {
  padding: 5px;
  /*
  margin-bottom:70px;
  margin-left: auto;
  margin-right: auto;*/
}
</style>
  