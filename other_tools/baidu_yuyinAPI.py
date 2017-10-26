from pydub import AudioSegment
import requests, json, base64
import uuid
import base64
import json
import urllib.request

# ./download/170531-110526.mp3


class BaiduYuYin(object):
    api_url = 'http://vop.baidu.com/server_api'
    header = 'Content-Type:application/json'
    post = {
        "format": "wav",
        "rate": 8000,
        "channel": 1,
        "token": 'xxx',
        "cuid": "baidu_workshop",
        "len": 4096,
        "speech": "xxx",
    }
    appID = '9708701'
    apiKey = 'I7pGNtYH68qXxEDvucsG72SU'
    secretKey = '9db8f5586a051df34ab86f3d016019b7'

    def __init__(self):
        pass

    @staticmethod
    def encodeBase64(path):
        with open(path, 'rb') as f:
            speech_data = f.read()
            # base64 编码
            raw_length = len(speech_data)
            speech_base64 = base64.b64encode(speech_data).decode('utf-8')
            print(speech_data)
            print(speech_base64, raw_length)
            return speech_base64, raw_length


    @staticmethod
    def formatParse(speech_path):
        input_path = speech_path
        fileName = speech_path.split('/')[-1]
        output_path = './download/output/'+fileName
        sound = AudioSegment.from_file(input_path, format="mp3")
        file_handle = sound.export(output_path, format="wav")

        print('转化文件中..', input_path)
        print('转化成功', output_path)

        speech_base64, raw_length = BaiduYuYin.encodeBase64(output_path)
        print('base64加密完成', output_path)

        # return input_path, BaiduYuYin.encodeBase64(input_path), raw_length

        return output_path, speech_base64, raw_length


    @staticmethod
    def getAccessToken():
        url = "https://openapi.baidu.com/oauth/2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": BaiduYuYin.apiKey,
            "client_secret": BaiduYuYin.secretKey,
        }
        # TODO token可以进行时效性判断
        r = requests.post(url, data=payload)
        r_dict = eval(r.content.decode('utf-8'))
        # print(r_dict['access_token'], r_dict)
        access_token = r_dict['access_token']
        return access_token


    @classmethod
    def upload_baiduyuyin(cls, speech_path):
        output_path, speech_base64, speech_length = BaiduYuYin.formatParse(speech_path)
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        access_token = BaiduYuYin.getAccessToken()
        data_dict = {'format': 'wav',
                     'rate': 8000,
                     'channel': 1,
                     'cuid': mac_address,
                     'token': access_token,
                     'lan': 'zh',
                     'speech': speech_base64,
                     'len': speech_length
                     }
        json_data = json.dumps(data_dict).encode('utf-8')
        json_length = len(json_data)
        request = urllib.request.Request(url=BaiduYuYin.api_url)
        request.add_header("Content-Type", "application/json")
        request.add_header("Content-Length", json_length)
        fs = urllib.request.urlopen(url=request, data=json_data)

        result_str = fs.read().decode('utf-8')
        json_resp = json.loads(result_str)
        print(json_resp, type(json_resp))

        return json_resp

    @classmethod
    def voice2msg(cls, speech_path):
        json_resp = BaiduYuYin.upload_baiduyuyin(speech_path)
        err_no = json_resp['err_no']
        if err_no == 0:
            result = json_resp['result']
            print(result)
            return result
        else:
            err_msg = json_resp['err_msg']
            print(err_msg)

    @classmethod
    def msg2voice(cls, text):
        url = "http://tsn.baidu.com/text2audio"
        access_token = BaiduYuYin.getAccessToken()
        mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
        # 2. 向Rest接口提交数据
        data = {'tex': text,
                'lan': 'zh',
                'cuid': mac_address,
                'ctp': 1,
                'tok': access_token,
                'per': 4
                }

        try:
            r = requests.post(url, data=data, stream=True, timeout=5)
            voice_fp = open('./download/Hi.mp3', 'wb')
            voice_fp.write(r.raw.read())
            # for chunk in r.iter_content(chunk_size=1024):
            # voice_fp.write(chunk)
            voice_fp.close()
            return True
        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout')
            return False
        except requests.exceptions.Timeout:
            print('Timeout')
            return False


    #     url = 'http://tsn.baidu.com/text2audio'
    #     mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    #     access_token = BaiduYuYin.getAccessToken()
    #     data_dict = {'tex': text,
    #                  'lan': 'zh',
    #                  'tok': access_token,
    #                  'ctp': 1,
    #                  'cuid': mac_address,
    #                  'per': 4
    #                  }
    #     json_data = json.dumps(data_dict).encode('utf-8')
    #     json_length = len(json_data)
    #     request = urllib.request.Request(url=BaiduYuYin.api_url)
    #     request.add_header("Content-Type", "application/json")
    #     request.add_header("Content-Length", json_length)
    #     fs = urllib.request.urlopen(url=url, data=json_data).read()
    #
    #     print(fs)








if __name__ == "__main__":
    # BaiduYuYin.upload_baiduyuyin()
    BaiduYuYin.msg2voice('你好，我是肖雄，我16岁啦!')

    #
    # import uuid
    # import base64
    # import json
    # import urllib.request
    #
    # asr_server = 'http://vop.baidu.com/server_api'
    # access_token = BaiduYuYin.getAccessToken()
    # mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    #
    # with open('./download/output/xiaoxiong_gay.wav', 'rb') as f:
    #     speech_data = f.read()
    #     speech_base64 = base64.b64encode(speech_data).decode('utf-8')
    #     speech_length = len(speech_data)
    #     data_dict = {'format': 'wav',
    #                  'rate': 8000,
    #                  'channel': 1,
    #                  'cuid': mac_address,
    #                  'token': access_token,
    #                  'lan': 'zh',
    #                  'speech': speech_base64,
    #                  'len': speech_length}
    #     json_data = json.dumps(data_dict).encode('utf-8')
    #     json_length = len(json_data)
    #     request = urllib.request.Request(url=asr_server)
    #     request.add_header("Content-Type", "application/json")
    #     request.add_header("Content-Length", json_length)
    #     fs = urllib.request.urlopen(url=request, data=json_data)
    #
    #     result_str = fs.read().decode('utf-8')
    #     json_resp = json.loads(result_str)
    #
    #
    # print(json_resp, type(json_resp))
