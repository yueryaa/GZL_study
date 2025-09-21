import OSS from 'ali-oss';
export function client() {
  var client = new OSS({
    region: 'oss-cn-beijing',
    accessKeyId: 'LTAI5tC38HLYH37oTfU5Z8oT',
    accessKeySecret: 'BSTLBiLuvG7z7j5FLS8qCrHsKoUxN0',
    bucket: 'userp'
  })
  return client
}