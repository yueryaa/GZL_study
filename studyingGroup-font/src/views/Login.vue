<template>
  <div class="background">
    <div class="login-body">
      <div class="login-panel" v-show="!isShowRegisterPanel">
        <div class="login-title">用户登录</div>
        <el-form :model="loginFormData" :rules="loginRules" ref="loginFormRef">
          <el-form-item label="手机号" prop="account">
            <el-input
              placeholder="请输入手机号"
              v-model="loginFormData.account"
              size="large"
            >
              <template #prefix>
                <span class="iconfont icon-account"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              placeholder="请输入密码"
              v-model="loginFormData.password"
              size="large"
              type="password"
            >
              <template #prefix>
                <span class="iconfont icon-password"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="">
            <el-button type="primary" style="width: 100%" @click="login"
              >登录</el-button
            >
          </el-form-item>
          <el-form-item label="">
            <div class="register-btn" @click="showRegisterPanel">
              还没有账号？立即注册
            </div>
          </el-form-item>
        </el-form>
      </div>
      <div class="register-panel" v-show="isShowRegisterPanel">
        <div class="register-title">用户注册</div>
        <el-form
          :model="registerFormData"
          :rules="registerRules"
          ref="registerFormRef"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              placeholder="请输入用户名"
              v-model="registerFormData.username"
              size="large"
            >
              <template #prefix>
                <span class="iconfont icon-account"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              placeholder="请输入密码"
              v-model="registerFormData.password"
              size="large"
              type="password"
            >
              <template #prefix>
                <span class="iconfont icon-password"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              placeholder="请再次输入密码"
              v-model="registerFormData.confirmPassword"
              size="large"
              type="password"
            >
              <template #prefix>
                <span class="iconfont icon-password"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input
              placeholder="请输入手机号"
              v-model="registerFormData.phone"
              size="large"
            >
              <template #prefix>
                <span class="iconfont icon-phone"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input
              placeholder="请输入邮箱"
              v-model="registerFormData.email"
              size="large"
            >
              <template #prefix>
                <span class="iconfont icon-email"></span>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="">
            <el-button type="primary" style="width: 100%" @click="register"
              >注册</el-button
            >
          </el-form-item>
          <el-form-item label="">
            <div class="login-btn" @click="hideRegisterPanel">
              已有账号？立即登录
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
  
  <script>
import CryptoJS from "crypto-js";
import qs from "querystring";
import { useRouter } from "vue-router";
import { inject } from "vue";
//import store from '../store'
const secretKey = "ThisIsAStrongAndSecureSecretKey12345";
const router = useRouter();

export default {
  data() {
    return {
      axios: inject("axios"),
      isShowRegisterPanel: false,
      loginFormData: {
        account: "",
        password: "",
        checkcode: "",
        rememberMe: false,
      },
      registerFormData: {
        username: "",
        password: "",
        confirmPassword: "",
        phone: "",
        email: "",
      },
      loginRules: {
        account: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            pattern: /^1\d{10}$/,
            message: "请输入11位手机号",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            pattern: /^(?=.*[a-zA-Z])(?=.*\d).{6,}$/,
            message: "密码必须包含字母和数字，且长度至少为6位",
            trigger: "blur",
          },
        ],
      },
      registerRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            pattern: /^(?=.*[a-zA-Z])(?=.*\d).{6,}$/,
            message: "密码必须包含字母和数字，且长度至少为6位",
            trigger: "blur",
          },
        ],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            pattern: /^1\d{10}$/,
            message: "请输入11位手机号",
            trigger: "blur",
          },
        ],
        email: [
          { required: true, message: "请输入邮箱", trigger: "blur" },
          { type: "email", message: "邮箱格式不正确", trigger: "blur" },
        ],
        confirmPassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          { validator: this.validateConfirmPassword, trigger: "blur" },
        ],
      },
    };
  },

  methods: {
    validateConfirmPassword(rule, value, callback) {
      if (value !== this.registerFormData.password) {
        callback(new Error("两次输入的密码不一致"));
      } else {
        callback();
      }
    },
    login() {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          // 对密码进行加密
          const encryptedPassword = CryptoJS.AES.encrypt(
            this.loginFormData.password,
            secretKey
          ).toString();

          // 构造加密后的登录数据
          const encryptedLoginData = {
            account: this.loginFormData.account,
            password: encryptedPassword,
          };

          console.log(encryptedLoginData);
          const jsonLoginData = JSON.stringify(encryptedLoginData);
          console.log(jsonLoginData); // 输出转化后的 JSON 字符串
          // 发送登录请求
          this.axios
            .post("/login/", qs.stringify(encryptedLoginData))
            .then((response) => {
              // 处理登录成功的逻辑
              console.log(response);
              if (response.data.state == 0) {
                alert(response.data.msg);
              } else {
                const decryptedPassword_user = CryptoJS.AES.decrypt(
                  response.data.pwd,
                  secretKey
                ).toString(CryptoJS.enc.Utf8); // 对用户中
                if (decryptedPassword_user == this.loginFormData.password) {
                  const account = response.data.state;
                  const accountStr = String(response.data.state);
                  if (account) {
                    localStorage.setItem("uid", accountStr);
                    const accountStr1 = localStorage.getItem("uid");
                    console.log(typeof accountStr1, accountStr1);
                  }
                  this.$store.state.isLogin = true;
                  console.log("store", this.$store.state.isLogin);
                  this.$router.push(`/${account}`);
                } else {
                  alert("密码错误，请重新输入！");
                }
              }
            })
            .catch((error) => {
              // 处理登录失败
              console.error("登录失败", error);
              alert(error);
            });
        }
      });
    },
    showRegisterPanel() {
      this.isShowRegisterPanel = true;
    },
    hideRegisterPanel() {
      this.isShowRegisterPanel = false;
    },
    register() {
      this.$refs.registerFormRef.validate((valid) => {
        if (valid) {
          // 对密码进行加密
          const encryptedPassword = CryptoJS.AES.encrypt(
            this.registerFormData.password,
            secretKey
          ).toString();
          const encryptedConfirmPassword = CryptoJS.AES.encrypt(
            this.registerFormData.confirmPassword,
            secretKey
          ).toString();

          // 构造加密后的注册数据
          const encryptedRegisterData = {
            name: this.registerFormData.username,
            password: encryptedPassword,
            account: this.registerFormData.phone,
            email: this.registerFormData.email,
            picture: "https://userp.oss-cn-beijing.aliyuncs.com/17045373920000",
          };
          const jsonRegisterData = JSON.stringify(encryptedRegisterData);

          // 发送注册请求
          this.axios
            .post("/signup/", qs.stringify(encryptedRegisterData))
            .then((response) => {
              // 处理注册成功的逻辑
              console.log(encryptedRegisterData);
              if (response.data.state[0] == 0) {
                alert(response.data.msg);
              } else {
                alert(response.data.msg);
              }
            })
            .catch((error) => {
              // 处理注册失败的逻辑
              alert(error);
            });
        }
      });
    },
  },
};
</script>
  
  <style scoped>
.background {
  background-image: url(../assets/bg.jpg);
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-body {
  position: absolute;
  top: 200px;
  right: 150px;
  width: 400px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
.login-panel,
.register-panel {
  padding: 30px;
}

.login-title,
.register-title {
  font-size: 20px;
  text-align: center;
  margin-bottom: 20px;
}

.checkcode-panel {
  display: flex;
  align-items: center;
}

.checkcode-panel1 {
  flex: 1;
}

.check-code {
  margin-left: 10px;
  height: 40px;
  cursor: pointer;
}

.register-btn,
.login-btn {
  text-align: center;
  cursor: pointer;
  color: #409eff;
}
</style>
  