import {
  createApp
} from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import Elementplus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/icon/iconfont.css'
import store from './store'
import axios from 'axios'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'



const app = createApp(App);
app.use(router);
app.use(Elementplus);
app.use(store);

app.config.globalProperties.Request = Request;



axios.defaults.baseURL = "http://123.57.2.117:8001"
app.provide('axios', axios)

//app.provide('globalTarget', 'http://192.168.43.149:8000/'); 

document.cookie = "myCookie=myValue; SameSite=Strict";

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}


app.mount('#app')