#======定义函数区=================================
#import library If报错重新安装下，运行sudo pip3 install --upgrade "google-cloud-kms"
from google.cloud import kms

#查找项目中某一个location里已有的密钥环
#GCP Console:菜单-security-Cryptographic keys
def getkeyringlist(project_id,location_id):
    from google.cloud import kms

# Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the parent location name.
    location_name = f'projects/{project_id}/locations/{location_id}'
    print(location_name)

    # Call the API.得到所有key_rings的类
    key_rings = client.list_key_rings(request={'parent': location_name})
# Example of iterating over key rings.遍历列出所有key_ring的信息
    for key_ring in key_rings:
        print(key_ring.name)
    return key_rings
#创建新密钥环
#GCP Console:菜单-security-Cryptographic keys
def create_key_ring(project_id, location_id, key_ring_id):
    #三个参数 均为string字符型
    from google.cloud import kms
    # Create the client.
    client = kms.KeyManagementServiceClient()
    # Build the parent location name.
    location_name = f'projects/{project_id}/locations/{location_id}'
    # Build the key ring.
    key_ring = {}
    # Call the API.创建一个新的key_ring
    created_key_ring = client.create_key_ring(request={'parent': location_name, 'key_ring_id': id, 'key_ring': key_ring})
    #打印出新密钥环的名字
    print('Created key ring: {}'.format(created_key_ring.name))
    return created_key_ring

 #创建非对称加密算法签名key
#创建非对称签名key
def create_key_asymmetric_sign(project_id, location_id, key_ring_id, key_id):
    client = kms.KeyManagementServiceClient()
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
    algorithm=algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_4096_SHA512
    key = {'purpose': purpose,'version_template': {'algorithm': algorithm, }}
    created_key = client.create_crypto_key(request={'parent': key_ring_name, 'crypto_key_id': key_id, 'crypto_key': key})
    print('Created asymmetric signing key: {}'.format(created_key.name))
    return created_key







   #----------------执行函数区------------------ 
#项目ID号，String,不是数字的project number
project_id='google.com:my-first-project-demo'
location_id='asia1'
key_id='rsakey'
key_ring_id='test' #key_ring_id (string): 就是在console中看到的name
#create_key_ring(project_id,location_id,key_ring_id)
getkeyringlist(project_id,location_id)
#create_key_asymmetric_sign(project_id,location_id,key_ring_id,key_id)

   
