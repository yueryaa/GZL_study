import OSS from 'ali-oss';
export function client() {
  var client = new OSS({
    region: 'oss-cn-beijing',
    accessKeyId: '***',
    accessKeySecret: '***',
    bucket: 'userp'
  })
  return client

}
