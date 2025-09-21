import {
  createRouter,
  createWebHistory
} from 'vue-router'
import store from '../store'
const routes = [{
    name: '登陆',
    path: '/logging',
    component: () => import('../views/Login.vue'),
  },
  {
    name: '首页',
    path: '/first',
    component: () => import('../views/firstpage.vue'),
  },
  {
    name: 'layout',
    path: '/',
    component: () => import('../views/Layout.vue'),
    children: [{
        name: 'home',
        path: '/home/:uid',
        component: () => import('../views/myHome.vue'),
      },
      {
        name: 'edit',
        path: '/edit/:uid',
        component: () => import('../views/editUser.vue'),
      },
      {
        name: 'homepage',
        path: '/:uid',
        component: () => import('../views/HomePage.vue'),
      },
      {
        name: 'friendcircle',
        path: '/:uid/:gid/:is_admin',
        component: () => import('../views/Arcitals/FriendCircle.vue'),
      },
      {
        name: 'writePost',
        path: '/:uid/writepost',
        component: () => import('../views/WritePost.vue'),
      },
      {
        name: 'updatePost',
        path: '/:uid/updatepost/:aid',
        component: () => import('../views/UpdatePost.vue'),
      },
    ]
  }
];

const router = createRouter({
  routes,
  history: createWebHistory(),
})


router.beforeEach((to, from, next) => {
  // console.log(to,from)
  // if(to.name==='xinwen' || to.name==='xiaxoi') 这种写法也可以
  console.log('store-router', store.state.isLogin)
  const uid = to.params.uid;
  if ((to.name === 'homepage' || to.name === 'home' || to.name === 'edit' || to.name === 'friendcircle' ||
      to.name === 'writePost' || to.name === 'updatePost' || to.name === 'layout') &&
    !store.state.isLogin) {
    next('/first')
  } else {
    next()
  }
})


export default router