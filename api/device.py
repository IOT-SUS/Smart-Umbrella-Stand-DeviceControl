import requests
from dateutil import parser

DEVICE_ID       = "1386424c"
SERVER_BASE_URL = "http://127.0.0.1:5000/api/"

class deviceAPI():
    @staticmethod
    def polling(success_func, faild_func):
        url = SERVER_BASE_URL + "rrs/polling/action/0/device/" + DEVICE_ID
        res = requests.get(url)

        if res.status_code == 200:
            return success_func(res)
        return faild_func(res)

    @staticmethod
    def rentSuccess(data, success_func, faild_func):
        url = SERVER_BASE_URL + "rent/success/" + DEVICE_ID
        res = requests.post(url, json=data)

        if res.status_code == 200:
            return success_func(res)
        return faild_func(res)

    @staticmethod
    def ureturn(data, success_func, faild_func):
        url = SERVER_BASE_URL + "return/" + DEVICE_ID
        res = requests.post(url, json=data)

        if res.status_code == 200:
            return success_func(res)
        return faild_func(res)

    @staticmethod
    def returnSuccess(data, success_func, faild_func):
        url = SERVER_BASE_URL + "return/success/" + DEVICE_ID
        res = requests.post(url, json=data)

        if res.status_code == 200:
            return success_func(res)
        return faild_func(res)
    
    @staticmethod
    def updateDeviceStatus(data, success_func, faild_func):
        url = SERVER_BASE_URL + "device/update_status/" + DEVICE_ID
        res = requests.post(url, json=data)

        if res.status_code == 200:
            return success_func(res)
        return faild_func(res)