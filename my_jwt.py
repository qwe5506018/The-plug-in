import json
import base64
import hmac
import copy
import time


class Jwt():
    def __init__(self):
        pass

    @staticmethod
    def encode(my_payload,key,exp=300):
        #初始化头部
        header = {"typ":"JWT","alg":"HS256"}
        header_json = json.dumps(header,sort_keys=True,separators=(",",":"))
        #第一个参数 按结果排序,第二个参数 把空格切了
        #sort_keys True  保证了json串输出时,按字符串顺序排序
        #separators  第一个参数是 每个键值对之间用什么分割,
        #第二个参数 指的是key和value之间 用什么分割- 通过该参数 -降低json串中的无效字符串[空格]
        header_bs = Jwt.b64encode(header_json.encode())
        #生成payload传进来参数是字典
        payload = copy.deepcopy(my_payload)
        payload["exp"] = time.time() + exp
        payload_json = json.dumps(payload,sort_keys=True,separators=(",",":"))
        payload_bs = Jwt.b64encode(payload_json.encode())

        #生成 hmac签名
        hm = hmac.new(key.encode(), header_bs + b"." + payload_bs,digestmod="SHA256")
        hm_bs = Jwt.b64encode(hm.digest())
        return header_bs + b"." + payload_bs + b"." + hm_bs

    @staticmethod
    def b64encode(j_s):
            #重写b64encode(j_s)
        return base64.urlsafe_b64encode(j_s).replace(b"=",b"")

    @staticmethod
    def b64decode(b_s):
        rem = len(b_s) % 4
        if rem>0:
            b_s = b"=" * (4-rem)
            #反向解析回来
        return base64.urlsafe_b64decode(b_s)

    @staticmethod
    def decode(token,key):
        #校验签名
        header_bs,payload_bs,sign_bs = token.split(b".")
        hm = hmac.new(key.encode(),header_bs + b"." + payload_bs,digestmod="SHA256")
        if sign_bs != Jwt.b64encode(hm.digest()):
            raise


        #检查token是否过期
        payload_json = Jwt.b64decode(payload_bs)
        payload = json.loads(payload_json)
        if "exp" in payload:
            now = time.time()
            if now > payload["exp"]:
                #过期
                raise
            #一切正常 则返回 payload部分的字典
        return payload





if __name__ == '__main__':
    s = Jwt.encode({"username":"hangming"},"123456")
    # print(s)
    print(Jwt.decode(s,"123456"))



