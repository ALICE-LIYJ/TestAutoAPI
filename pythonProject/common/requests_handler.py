import requests
class RequestHandler:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def visit(self,method,url,params = None,data=None,json=None,headers=None):
        result = self.session.request(method,url,params=params,data=data,json=json,headers=headers,verify=False)
        try:
            #返回json结果
            print(result)
            return result.json()
        except Exception:
            return 'not json'
    def close_session(self):
        self.session.close()