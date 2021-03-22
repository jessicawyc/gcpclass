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
def create_key(project_id, location_id, key_ring_id, key_id,key_usage):
    client = kms.KeyManagementServiceClient()
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)
    """
    #Purpose指定密钥的用途，主要分为以下三种，请根据需要选，#algorithm为密钥指定的算法，需要与purpose对应
    #非对称数字签名，支持椭圆曲线和RSA等多种哈希hash摘要长度
    purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN
   
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EC_SIGN_P256_SHA256
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EC_SIGN_P384_SHA256
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PSS_3072_SHA256
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PKCS1_4096_SHA512

    #非对称解密
    purpose = kms.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT

    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_3072_SHA256
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_4096_SHA256
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_DECRYPT_OAEP_4096_SHA512

    #对称加密和解密， 使用默认AES-256 GCM算法，无法选择其它不安全的算法或更短的key
    purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    
    algorithm = kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.EXTERNAL_SYMMETRIC_ENCRYPTION

    更多详情or更新请以官网为准
    https://cloud.google.com/kms/docs/algorithms
    """
    
    purpose = kms.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT
    algorithm=kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    
    
  
    key = {'purpose': purpose,'version_template': {'algorithm': algorithm, },'labels': {
            'team': 'ITteam1',
            'cost_center': 'cc1234',
            'conf_L':'Secret'}} #labels会出现在BIll账单中，适用作为分账的标记，也可以标识机密级别
    created_key = client.create_crypto_key(request={'parent': key_ring_name, 'crypto_key_id': key_id, 'crypto_key': key})
    print('Created asymmetric signing labeled key: {}'.format(created_key.name))
    return created_key
#给key设定rotation schedule自动轮换密钥周期的计划以及第一次轮换时间,完成后进入console-key会看到rotation period和 next rotation均会更新
def update_key_add_rotation(project_id, location_id, key_ring_id, key_id,rotationtime,nexttime):
    """
    
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string):  就是在console中看到的name (e.g. 'my-key-ring').
        key_id (string): ID of the key to use console中看到的key name(e.g. 'my-key').
        nexttime（数值）:下一次开始轮换的时间，以秒计算，1天应为60*60*24 
        rotationtime（数值）：轮换周期，每到这些天就自动轮换一次，以秒计算，30天为=60*60*24*30

    Returns:
        CryptoKey: Updated Cloud KMS key.

    """

    # Import the client library.
    from google.cloud import kms

    # Import time for getting the current time.
    import time

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key name.
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    key = {
        'name': key_name,
        'rotation_period': {
            'seconds': rotationtime  # Rotate the key every 30 days.周期以秒计算，要换算
        },
        'next_rotation_time': {
            'seconds': int(time.time()) + nexttime  # Start the first rotation in 24 hours.首次轮换开始时间
        }
    }

    # Build the update mask.
    update_mask = {'paths': ['rotation_period', 'next_rotation_time']}

    # Call the API.
    updated_key = client.update_crypto_key(request={'crypto_key': key, 'update_mask': update_mask})
    print('Updated key: {}'.format(updated_key.name))
    return updated_key






   #----------------执行函数区------------------ 
#项目ID号，String,不是数字的project number
project_id='google.com:yourprojectname'
location_id='global'
key_usage='ASYMMETRIC_SIGN'
key_ring_id='mykeys' #key_ring_id (string): 就是在console中看到的name
key_id='labedkey'
nexttime=60*60*24 #24小时=1day
rotationtime=60*60*24*50 #50天
#create_key_ring(project_id,location_id,key_ring_id)
#getkeyringlist(project_id,location_id)
#create_key(project_id,location_id,key_ring_id,key_id)
#update_key_add_rotation(project_id, location_id, key_ring_id, key_id,rotationtime,nexttime)

   
