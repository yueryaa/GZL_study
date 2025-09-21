import Mock from 'mockjs'
import CryptoJS from 'crypto-js'
import qs from 'querystring';

/*
Mock.setup({
    timeout:4000
})*/
Mock.mock('http://192.168.43.149:8000/signup', 'post', {
    code: 200,
    message: '注册成功',
    data: {
      username: '@cname',
      password: '@string("lower", 6)',
      phone: /^1[385][1-9]\d{8}/,
      email: /\w+@[a-z0-9]+\.[a-z]{2,3}/
    }
  })

// 定义密钥
const secretKey = 'ThisIsAStrongAndSecureSecretKey12345'

// 定义密钥

// 模拟用户数据库
const users = [
  {
    account: '1',
    password: CryptoJS.AES.encrypt('1', secretKey).toString()  // 对密码进行加密存储
  },
  {
    account: '2',
    password: CryptoJS.AES.encrypt('2', secretKey).toString()
  }
]

// 登录接口
Mock.mock('http://192.168.43.149:8000/login', 'post', (req) => {
  const { account, password } = JSON.parse(req.body)
  const decryptedPassword_user = CryptoJS.AES.decrypt(password, secretKey).toString(CryptoJS.enc.Utf8)  // 对用户中的加密密码进行解密
   //const user = users.find(u => u.account === account && u.password === password)
  const user = users.find(u => u.account === account)
  const decryptedPassword = CryptoJS.AES.decrypt(user.password, secretKey).toString(CryptoJS.enc.Utf8)  // 对数据库中的加密密码进行解密
  //console.log(decryptedPassword,'shujuku')
  if (decryptedPassword == decryptedPassword_user) {
    return {
      state: 200,
      msg: '登录成功',
      account:user.account,
    }
  } else {
    return {
      state: 400,
      message: '用户名或密码错误'
    }
  }
})

// 使用正则表达式匹配接口
Mock.mock(/\/file\/getAvatar\/\d+/, 'get', () => {
  // 生成一个随机的base64编码图片数据
  const image = Mock.Random.dataImage('60x60', 'Avatar');
  // 模拟一个HTTP响应
  return {
    status: 200,
    data: image
  };
});

//用户信息返回
// 设置拦截规则和返回数据

Mock.mock(/\/UserDetail\/\?id=\d+/, 'get', function(options) {
  const id = options.url.match(/\/UserDetail\/\?id=(\d+)/)[1];

  if (id === '404') {
    return Mock.mock({
      'status': 404,
      'message': '用户不存在'
    });
  } else {
    return Mock.mock({
      data: {
        'id': id,
        'currentIntegral|1-100':100,
        "likeCount|1-100": 100,
        "postCount|1-100": 100,
        "collectCount|1-100": 100,
        'password': '@word(6, 10)',
        'remark': '@sentence(5, 10)',
        'account': '@word(5, 8)',
        'birthday': '@date("yyyy-MM-dd")',
        'sex|1': ['0', '1'],
        'name': '@cname'
      }
    });
  }
});


//跟新用户信息
Mock.mock(/\/UserDetail\//, 'put', {
  code: 200,
  message: '保存成功'
});

//排行榜
// rankArtical 接口
Mock.mock(/\/rankArtical\/\?gid=\d+/, 'get', (options) => {
  //const gid = options.url.match(/\/rankArtical\/\?gid=(\d+)/)[1];

  // 根据参数 gid 生成模拟数据
  const data = Mock.mock({
    code: 200,
    msg: 'success',
    'data|5-10': [{
      'rank|+1': 1,
      'name': '@cname',
      "number|1-100": 100,
      'avatar': '@image("50x50")'
    }]
  })

  // 返回仅包含排名、名称和图片的数据结构
  const result = data.data.map(item => ({
    rank: item.rank,
    name: item.name,
    number:item.number,
    avatar: item.avatar
  }))

  return {
    code: data.code,
    msg: data.msg,
    data: result
  }
})
//点赞
Mock.mock(/\/rankLike\/\?gid=\d+/, 'get', (options) => {
  //const gid = options.url.match(/\/rankArtical\/\?gid=(\d+)/)[1];

  // 根据参数 gid 生成模拟数据
  const data = Mock.mock({
    code: 200,
    msg: 'success',
    'data|5-10': [{
      'rank|+1': 1,
      'name': '@cname',
      "number|1-100": 100,
      'avatar': '@image("50x50")'
    }]
  })

  // 返回仅包含排名、名称和图片的数据结构
  const result = data.data.map(item => ({
    rank: item.rank,
    name: item.name,
    number:item.number,
    avatar: item.avatar
  }))

  return {
    code: data.code,
    msg: data.msg,
    data: result
  }
})

//小组名称
//点赞
Mock.mock(/\/User_GroupDetail\/\?gid=\d+/, 'get', (options) => {
  //const gid = options.url.match(/\/rankArtical\/\?gid=(\d+)/)[1];

  // 根据参数 gid 生成模拟数据
  const data = Mock.mock({
    code: 200,
    msg: 'success',
    'data': [{
      'gid|+1': 1,
      'group_name': '@word(5)',
      "id|1-10": [
        {
          "id|+1": [
            "1",
            "2",
            "3"
          ]
        }
      ],
      "name|1-10": [
        {
          "id|+1": [
            "张三",
            "李四",
            "赵武"
          ]
        }
      ]
    }]
  })

  return Mock.mock({
    data:{
      'gid|+1': 1,
      'group_name': '@word(5)',
      "id|1-10": [
        {
          "id|+1": [
            "1",
            "2",
            "3"
          ]
        }
      ],
      "name|1-10": [
        {
          "id|+1": [
            "张三",
            "李四",
            "赵武"
          ]
        }
      ]
    }
  });
})


//返回文章内容
Mock.mock(/loadArctial\/\?gid=\d+/, 'get', (options) => {
  const Random = Mock.Random;
  const data =  Mock.mock({
    'data|1-10': [
    {
      "aid|1-100": 100,
      "uid|1-2": 2,
      'User_name': '@cname',
      'image': '@image("50x50")',
      'content': '@cparagraph',
      'aimage|0-4': ['@image("300x200")'],
      //'@image("200x100")', '@image("100x50")', '@image("150x80")','@image("100x100")'
      'atime': '@datetime',
      'likeList|0-9': ['@cname'],
      'commentList|0-9': [
        {
          commenter: '@cname',
          comment: '@cparagraph',
        },
      ],
    },
  ]
  });
  return data;

});

//返回自己文章内容
Mock.mock(/\/getownArtical\/\?id=\d+/, 'get', function(options) {
  const data =  Mock.mock({
    'data|1-5': [
    {
      'gid|1-9':9,
      "aid|1-100": 100,
      "uid|1-2": 2,
      'User_name': '@cname',
      'image': '@image("50x50")',
      'content': '@cparagraph',
      'aimage|0-4': ['@image("300x200")'],
      //'@image("200x100")', '@image("100x50")', '@image("150x80")','@image("100x100")'
      'atime': '@datetime',
      'likeList|0-9': ['@cname'],
      'commentList|0-9': [
        {
          commenter: '@cname',
          comment: '@cparagraph',
        },
      ],
    },
  ]
  });
  return data;
});

//返回点赞文章内容
Mock.mock(/\/getownlikeArtical\/\?id=\d+/, 'get', function(options) {
  const data =  Mock.mock({
    'data|1-5': [
    {
      'gid|1-9':9,
      "aid|1-100": 100,
      "uid|1-2": 2,
      'User_name': '@cname',
      'image': '@image("50x50")',
      'content': '@cparagraph',
      'aimage|0-4': ['@image("300x200")'],
      //'@image("200x100")', '@image("100x50")', '@image("150x80")','@image("100x100")'
      'atime': '@datetime',
      'likeList|0-9': ['@cname'],
      'commentList|0-9': [
        {
          commenter: '@cname',
          comment: '@cparagraph',
        },
      ],
    },
  ]
  });
  return data;
});
//返回收藏文章内容
Mock.mock(/\/getowncollectArtical\/\?id=\d+/, 'get', function(options) {
  const data =  Mock.mock({
    'data|1-5': [
    {
      'gid|1-9':9,
      "aid|1-100": 100,
      "uid|1-2": 2,
      'User_name': '@cname',
      'image': '@image("50x50")',
      'content': '@cparagraph',
      'aimage|0-4': ['@image("300x200")'],
      //'@image("200x100")', '@image("100x50")', '@image("150x80")','@image("100x100")'
      'atime': '@datetime',
      'likeList|0-9': ['@cname'],
      'commentList|0-9': [
        {
          commenter: '@cname',
          comment: '@cparagraph',
        },
      ],
    },
  ]
  });
  return data;
});


//点赞
// 拦截 /likeArctical/ 的POST请求
Mock.mock('http://192.168.43.149:8000/likeArctical/', 'post', (config) => {
  // 将请求参数从URL编码的字符串转换为JSON对象
  const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})

// 拦截 /likeArctical/ 的DELETE请求
Mock.mock('http://192.168.43.149:8000/likeArctical/', 'delete', (config) => {
  const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})

//收藏
// 拦截 /collectArctical/ 的POST请求
Mock.mock('http://192.168.43.149:8000/collectArctical/', 'post', (config) => {
  // 将请求参数从URL编码的字符串转换为JSON对象
  const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})

// 拦截 /collectArctical/ 的DELETE请求
Mock.mock('http://192.168.43.149:8000/collectArctical/', 'delete', (config) => {
  const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})
//评论文章
Mock.mock('http://192.168.43.149:8000/commentArctical/', 'post', (config) => {
  // 将请求参数从URL编码的字符串转换为JSON对象
  //const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})

//删除文章
Mock.mock('http://192.168.43.149:8000/delectArctical/', 'delete', (config) => {
  const { gid, uid, aid, currentime } = qs.parse(config.body)
  return {
    status: 1,
    msg: 'success',
  }
})


Mock.mock("http://192.168.43.149:8000/user_group/",
  [
    {
      gid: 1,
      group_name: "New kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
      id: 1,
      is_admin: 1
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 3,
      group_name: "New kkkkkkkkkkkk",
      id: 1,
      is_admin: 1
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 5,
      group_name: "New kkk",
      id: 1,
      is_admin: 1
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 5,
      group_name: "New kkk",
      id: 1,
      is_admin: 1
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    },
    {
      gid: 5,
      group_name: "New kkk",
      id: 1,
      is_admin: 1
    },
    {
      gid: 2,
      group_name: "aaa",
      id: 1,
      is_admin: 0
    }
  ]
);
Mock.mock("http://192.168.43.149:8000/User_GroupDetail/", {
  msg: "删除成功",
  data: [
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'John Smith',
      id: 10
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
      id: 3
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'bbbbbbbb',
      id: 10
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'ccccccc',
      id: 3
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'ddd',
      id: 10
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'eeeee',
      id: 3
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'fffff',
      id: 10
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'ggggg',
      id: 3
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'kkkkkk',
      id: 10
    },
    {
      gid: 1,
      group_name: 'jjjjjjj',
      user_name: 'ggggg',
      id: 3
    },

  ]
}
);
Mock.mock("http://192.168.43.149:8000/creat_group/",
  {
    "gid": 22,
    "name": "sfdaf",
    "number": 1,
    "id": 1
  }
);
Mock.mock("http://192.168.43.149:8000/ApplicationDetail/", {
  msg: "操作成功",
  data: [
    {
      id: 1,
      User_name: "aa",
      gid: 4,
      group_name: "aaaaa",
      msg: "我是xxx"
    },
    {
      id: 2,
      User_name: "bbbb",
      gid: 2,
      group_name: "mklmwohi",
      msg: "dbshiuagcbhusafghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    },
    {
      id: 1,
      User_name: "anjhubhg",
      gid: 4,
      group_name: "soiahuiwfgtyu",
      msg: "我是xxx"
    },
  ]
}
);
Mock.mock("http://192.168.43.149:8000/interaction_info/", {
  msg: "删除成功",
  data: [
    {
      id: 1,
      nid: 2,
      User_name: "aa",
      ncontent: "点赞"
    },
    {
      id: 1,
      nid: 3,
      User_name: "jwkuhqgi",
      ncontent: "评论"
    },
    {
      id: 1,
      nid: 8,
      User_name: "ccc",
      ncontent: "收藏"
    },
  ]
});
Mock.mock("http://192.168.43.149:8000/write_post/",
  {
    msg: "发布成功"
  }
);
Mock.mock("http://192.168.43.149:8000/update_post/",{
  msg:"修改成功",
  data: {
    aid: 2,
    id: 1,
    gid: 1,
    content: "dshuigwut",
    imageUrl: ['data:image/jpeg;base64,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'],
    atime: "2023/12/9 13:06:27"
  }
}
);