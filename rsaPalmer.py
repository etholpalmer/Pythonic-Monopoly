import sys
import os
from os import path
import rsa
import base64
from dotenv import load_dotenv, find_dotenv

Is_Win           = lambda    : sys.platform=='win32' or sys.platform=='cygwin'
Get_Env_Var      = lambda key: ((type(os.getenv(key)==str)), os.getenv(key))
Key_Is_Encrypted = lambda key: (key[-4:].lower() == '_enc')

if not Is_Win():
  default_path = '/content/drive/MyDrive/BootCampSpot/'
else:
  default_path = './'
print(f'Default Path = {default_path}')

# '/content/drive/MyDrive/BootCampSpot/.env'
default_env_file = path.join(default_path, '.env')
dot_env_exists = path.exists(default_env_file)
xistr = "exists" if dot_env_exists else "DOES NOT EXIST"
print(f'Default Env file Path = {default_env_file} {xistr}')

def bin_2_str(data:bytes):
  if data is None:
    return None
  return base64.b64encode(data).decode()
def str_2_bin(data:str):
  if data is None:
    return None
  return base64.b64decode(data.encode())

def Get_RSAKey(path_name=default_path, public_key=True, nbits=4096, create_keys=False):
    pub_file = path_name+'public.pem'
    prv_file = path_name+'private.pem'
    (pubkey, privkey) = (None,None)

    exist_pub = path.exists(pub_file)
    exist_prv = path.exists(prv_file)

    if exist_pub:
      print(f"Public file exists")

    if exist_prv:
      print(f"Private file exists")

    if (not exist_pub) and (not exist_prv):
      if create_keys:
        (pubkey, privkey) = rsa.newkeys(nbits)
        
        pub = pubkey.save_pkcs1()
        pubfile = open(pub_file,'w+')
        pubfile.write(pub.decode('UTF-8'))
        pubfile.close()
        
        pri = privkey.save_pkcs1()
        prifile = open(prv_file,'w+')
        prifile.write(pri.decode('UTF-8'))
        prifile.close() 

        if public_key:
          return pubkey
        else:
          return privkey
      else:
        print(f"Not creating file(s)")
        return None
    else:
      if public_key and exist_pub:
        # read and return the public key
        with open(pub_file) as fp:
          publicKey = rsa.PublicKey.load_pkcs1(fp.read().encode('UTF-8'))
        return publicKey
      elif (public_key==False) and exist_prv:
        # read and return the private key
        with open(prv_file) as fp:
          privateKey = rsa.PrivateKey.load_pkcs1(fp.read().encode('UTF-8'))
        return privateKey
      else:
        print(f"Didn't find the key to work with")

def Encrypt(data_2_enc:str = None, path_name=default_path):
    publicKey = Get_RSAKey(path_name=path_name)

    if (data_2_enc is None) or (publicKey is None):
        return None

    return rsa.encrypt(data_2_enc.encode('UTF-8'), publicKey)

def Decrypt(data_2_decrypt= None, path_name=default_path):
    privateKey = Get_RSAKey(path_name= path_name, public_key=False)

    if (data_2_decrypt is None) or (privateKey is None):
        return None

    return rsa.decrypt(data_2_decrypt, privateKey).decode()

def Get_API_Key(key_name="QUANDL_API_KEY_enc"
                , env_file=default_env_file
                , encrypted:bool=False
                , enc_file_path=default_path):

  if Key_Is_Encrypted(key=key_name):
    encrypted = True

  key_name_exists, val = Get_Env_Var(key=key_name)

  if not key_name_exists:
    if not Get_Env_Var(key='PalmerEnv')[0]:   # Tells if the Database Environment has NOT been loaded before
      if load_dotenv(find_dotenv(filename=env_file)): #, raise_error_if_not_found=True)):
        key_name_exists, val = Get_Env_Var(key=key_name)   # Try again
        if not key_name_exists:
          return False, (f'The key was not found "{key_name}" in [{env_file}]') 
      else:
        return False,  (f'enviroment file missing {env_file}')
    else:
      print(f'key not found {key_name}')
      return False, (f'key not found {key_name}')

  if encrypted:
    data_2_decrypt = str_2_bin(val)
    val = Decrypt(data_2_decrypt=data_2_decrypt, path_name=enc_file_path)

  return True, val

if __name__ == "__main__": 
    print (f"File {__name__} is being run directly")
    print('DATABASE_NAME', Get_API_Key(key_name='DATABASE_NAME', env_file='D:\\Data\\Family\\Ethol Palmer\\UoT SCS\\FinTech\\.env')[1])
    print('PalmerEnv', Get_API_Key('PalmerEnv')[1])
    print('QUANDL_API_KEY_enc', Get_API_Key('QUANDL_API_KEY_enc')[1])
    print('ALPACA_API_KEY_enc', Get_API_Key('ALPACA_API_KEY_enc')[1])
    print('ALPACA_SECRET_KEY_enc', Get_API_Key('ALPACA_SECRET_KEY_enc')[1])
    print('map_box_api', Get_API_Key('map_box_api')[1])
else: 
    print (f"File {__name__} is being imported")
# pub_key = Get_RSAKey(path_name=default_path, public_key=True, nbits=1024, create_keys=False)
# prv_key = Get_RSAKey(path_name=default_path, public_key=False)

# a = "9VjfsbEo0ck0rEEXKfO1q1o741jImYdLU596npEX"
# b = "C0BjqhyO34dxczkgiaSZeR9M6iTYHp+dcFYJfyfa4Rnr8rZi1cLYwtBqC+xfgpsC+n4fnaJze5sFJBym8yub0LwNXtW1YNjYDYVv18Mz9oEit1agxJPdTQ1ZAzBZBgXD7bohmqWKzkTEq3FvqyWVd9m80a5MPk+VypJQxL5j86L45aChYdDxqREYNHck8Gh2/7J9VG3YKsULKACO9UcTJy8wjGyMVL44srfZ6P1tgGJE0RDUEBtFt8xAhx/ganihOy+wc2yxA+m2YEzBACxYiT8nQCACCUTo3WghDmxq7O0xGFvvoFJNEwSKQIN/qqg5oj+2HxI8Yk+AIKN1anir4tU2N5y3XCYaJL57qKF+hOt8TUfPws4FwpDgS5pjiBKqaZNhYQIr2e2O8QtyFh6u4kuRTUjQ4lmsFpgQGrt7wa8yh/JrBtjmY0P46tpn45IMQyyMsJV4+RSm+lrQGdVC9bb58+0VwmOyRRg9Tk/BSKE8UdzcVT8idED14Zoq+lunNDy1C+GU9twrXqKDgSZkfYQVfzX2sy3ptdzrFdyUBu8C2+pkRTzTp13k9NOrt3aPGWQRy84xaP98s01+6jB2adgugU6LF5504IHR065hcSPete+PODmT8QM5reRN8m5tCGGdwH2+PpP6lmDovast4Ts0HkEHFxO7XtKryMPORlE="
# a_enc = Encrypt(a,default_path)

# print(a)
# print(a_enc)
# result = bin_2_str(a_enc)
# print(result)
# result_bin = str_2_bin(b)
# a_dec = Decrypt(result_bin,default_path)
# print(a_dec)
# print('Done',a==a_dec)