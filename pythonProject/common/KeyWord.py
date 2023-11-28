# -*- coding: UTF-8 -*-
import requests
import os, re, time
from pathlib import Path
import platform
import json
import logger
class PSPApi(object):

    @staticmethod
    def GetCookie(url, name, password):
        """
        获取psp cookie
        :param url: 网址
        :param name: 用户名
        :param password: 密码
        :return: cookie
        """
        name = name.encode("utf-8").decode("latin1")
        headers = {"Content-Type": "application/json; charset=UTF-8","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        payload = {"name": name,"password": password}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload),verify=False)
        #print(f"登录接口的返回值：{response.text}")
        if response.status_code == 200:
            # logger.info(f"登录返回cookie: {response.cookies.get_dict()}")
            dict_cookies = requests.utils.dict_from_cookiejar(response.cookies)
            cookiestr = ""
            for key in dict_cookies.keys():
                value = dict_cookies.get(key)
                if cookiestr == "":
                    cookiestr = key + "=" + value
                else:
                    cookiestr = cookiestr + ";" + key + "=" + value
            #print(f"获取psp cookie：{locals()}")
            if len(cookiestr) == 0:
                print(f"cookie是空的： {response.text}")
            return cookiestr
        else:
            print(f"获取psp cookie：{locals()}")
            print(f"获取psp cookie 返回值信息：{response.text}")
            print("response code" + str(response.status_code))
            print("登录失败")

    @staticmethod
    def SendHttpRequest(cookie, url, req_body=None):
        """
        发送http请求
        :param req_body: 请求时需手动把\改为\\\
        :return: response的string形式

        Example:
        | *Keywords*           |  *Parameters*  |
post请求 | Send Http Request    |cookie          |url            |req_body
get请求  | Send Http Request    |cookie          |url
        """

        headers = {
            'cookie': cookie,
            'cache-control': "no-cache"
        }
        print(f"请求的url: {url}")
        # 发送get请求
        if req_body is None:
            resp = requests.get(url, cookie, headers=headers)
        else:
            # 发送post请求,请求参数是json类型
            if req_body.startswith("{") or req_body.startswith("["):
                headers["Content-Type"] = "application/json;charset=UTF-8; charset=UTF-8"
                req_body = req_body.replace('false', 'False').replace('true', 'True')
                dict_pay = eval(req_body)
                # print("发送post请求，url为：" + url + "；请求参数为：" + req_body)
                resp = requests.request("POST", url, data=json.dumps(dict_pay), headers=headers)
            else:
                # 发送post请求,请求参数是Form_Data类型
                if req_body is not None:
                    req_body = req_body.encode("utf-8").decode("latin1")
                headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                # print("发送post请求，url为：" + url)
                # print("请求参数为："+ req_body)
                resp = requests.post(url, data=req_body, headers=headers)

        # if resp.json().get("result") != 1:    # 不清楚这个请求是不是只有erp系统中，避免返回的不是可转换为json格式
        #     logger.info(f"请求body是：{req_body}")
        #     logger.info(f"请求返回值是：{resp.text}")

        if str(resp.status_code) != "200":
            print(f"请求返回不是200-请求body是：{req_body}")
            print(f"请求返回不是200-请求返回值是：{resp.text}")
            # raise Exception("请求发送错误，status code:"+str(resp.status_code)+"；错误内容："+resp.text)
            return False
        else:
            print(f"请求的body是：{req_body}")
            print(f"请求返回值是：{resp.text}")
            return resp.text

    @staticmethod
    def SendHttpFile(cookie, url, filepath, filename, payload="{}"):
        """
        【导入文件】
        :param cookie:
        :param url:
        :param filepath: 文件放在目录TestData下，filepath为文件夹名称，比如ERP_Project\Erp\TestData\商品模块，则填 商品模块
        :param filename: 文件名
        :param payload: post请求的参数，比如{{'isSuite': '2'}}
        :return:

        Example:
        | *Keywords*       |  *Parameters* |
        | Send Http File   |cookie         |url           | filepath       |requestbody（optional）
        """
        try:
            if platform.system() == 'Windows':
                datapath = os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\TestData\\" + filepath
                file = datapath + "\\" + filename
            else:
                datapath = os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/TestData/" + filepath
                file = datapath + "/" + filename
            if os.path.isfile(file):
                files = [
                    ('file', (filename,
                              open(file, 'rb'),
                              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
                ]
                headers = {
                    'cookie': cookie
                }
                dict_pay = eval(payload)
                response = requests.request("POST", url, headers=headers, data=dict_pay, files=files)
                if str(response.status_code) != "200":
                    print("response code" + str(response.status_code))
                    print("结果错误：" + response.text)
                    return False
                else:
                    print("文件上传成功！")
                    print(response.text)
                return response.text
            else:
                raise FileNotFoundError
        except Exception as e:
            print("请求发送错误，原因是", e)

    @staticmethod
    def get_domain():
        """
        获取运行环境，读取UserVariable/通用.txt的${domain}变量
        """
        datapath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        if platform.system() == 'Windows':
            urlfilepath = datapath + r"\UserVariable\通用.txt"
        else:
            urlfilepath = datapath + r"/UserVariable/通用.txt"
        with open(urlfilepath, encoding='utf-8') as file:
            content = file.read()
            # result = re.findall('{url}            ([\S]*).superboss.cc', content)
            result = re.findall('https://([\S]*).superboss.cc', content)[0]
            return result

    @staticmethod
    def SendDownloadFile(cookie, url, req_body=None, filepath=None):
        """
        发送下载文件的请求,去下载中心下载
        :param cookie:
        :param url:
        :param req_body: 请求参数，如果是get请求可不填
        :param filepath: 保存文件到指定路径，不填默认保存到C:\Temp文件夹
        :return: 文件的保存路径
        """
        # 发送请求下载文件
        try:
            PSPApi.SendHttpRequest(cookie, url, req_body=req_body)

            url1 = url.split(".superboss")[0]
            # 等待文件下载完成
            schedule = "2"
            count = 0
            # 等待文件下载完成
            while schedule == "2" and count < 1000:  # schedule=2导出中  schedule=3导出完成 schedule=4 导出失败
                count += 1
                downcenter_url = url1 + '.superboss.cc/downloadCenter/list?api_name=downloadCenter_list&startDate=1612345890000&endDate=&module=&timeType=exportTime&schedules=&pageNo=1&pageSize=20'

                down_header = {"Content-Type": "application/json;charset=UTF-8",
                               'cookie': cookie}
                downlist = requests.get(downcenter_url, headers=down_header)
                schedule = PSPApi.GetResonseValue(downlist.text, "data.list[0].schedule")
                print("文件下载中，请稍候......(timeout=1000，已等待%s秒)" % (count))
                time.sleep(1)
                # 最多等候1000秒
            if schedule == "4":
                raise Exception("文件下载失败，请检查！")
            # 获取下载中心第一行数据的导出时间和第二行数据的导出时间,如果相同，则可能存在并发任务（导出一次，实际有2个下载任务）
            exportTime0 = PSPApi.GetResonseValue(downlist.text, "data.list[0].exportTime")
            exportTime1 = PSPApi.GetResonseValue(downlist.text, "data.list[1].exportTime")
            if exportTime0 == exportTime1:
                raise Exception("存在并发的导出任务，请检查下载中心")

            # 获取下载中心第一行数据的文件名
            filename = PSPApi.GetResonseValue(downlist.text, "data.list[0].content")
            time.sleep(2)
            fileUrl = "https://erp-tmp-zb.oss-cn-zhangjiakou.aliyuncs.com/" + filename

            # 获取excel内容
            result = PSPApi.get_domain()
            header2 = {"referer": "https: // " + result + ".superboss.cc/index.html"}
            ex_content = requests.get(fileUrl, headers=header2)

            # 下载文件到filepath对应的文件夹，如果filepath为None，默认下载到download文件夹
            if filepath is None:
                if platform.system() == 'Windows':
                    filepath = "C:\\Temp\\"
                else:
                    filepath = r"/home/ERP_RF/下载文件/"

            if Path(filepath).exists() is False:
                os.mkdir(filepath)
            # 部分模块导出的是csv文件，全部保存为excel格式，方便校验内容
            newfile = filename.replace('csv', 'xlsx')
            files = filepath + newfile

            fp = open(files, 'wb')
            fp.write(ex_content.content)
            fp.close()
            return files

        except Exception as e:
            print("请求错误，原因是", e)
            return e

    @staticmethod
    def GetProjectPath():
        """
        获取当前项目路径
        """
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        print("当前项目路径为：", project_path)
        return project_path

    @staticmethod
    def ResponseShouldBeEqual(resopnse, path, expectvalue):
        """
        判断请求结果是否等于预期值，相等返回True，不相等则报错
        :param resopnse: request的请求结果
        :param path: 要对比数据的路径，Property Path
        :param expectvalue: 预期值
        :return:
        """

        actualValue = PSPApi().GetResonseValue(resopnse, path)
        if actualValue == str(expectvalue):
            return True
        else:
            print("结果不相等,实际结果是：" + str(actualValue))
            print("预期结果是：" + str(expectvalue))
            raise AssertionError

    @staticmethod
    def ResponseShouldContain(resopnse, path, expectvalue):
        """
        判断请求结果是否包含预期值，包含返回True，不包含则报错
        :param resopnse: request的请求结果
        :param path: 要对比数据的路径，Property Path
        :param expectvalue: 预期值
        :return:
        """

        actualValue = PSPApi().GetResonseValue(resopnse, path)
        if expectvalue in str(actualValue):
            return True
        else:
            print("校验失败,实际结果是：" + str(actualValue))
            print("未包含预期字符串：" + str(expectvalue))
            raise AssertionError

    @staticmethod
    def ResponseShouldBeTrue(resopnse, path):
        """
        判断请求结果是否为True
        :param resopnse: request的请求结果
        :param path: 要对比数据的路径，Property Path
        :return:
        """

        actualValue = PSPApi().GetResonseValue(resopnse, path)
        if actualValue is True:
            return True
        else:
            print("校验失败,预取结果是：True,返回" + str(actualValue))
            raise AssertionError

    @staticmethod
    def ResponseShouldBeEmpty(resopnse, path):
        """
        判断请求结果是否为空
        :param resopnse: request的请求结果
        :param path: 要对比数据的路径，Property Path
        :return:
        """

        actualValue = PSPApi().GetResonseValue(resopnse, path)
        if actualValue == "":
            return True
        else:
            print("校验失败,预期结果为空,返回" + str(actualValue))
            raise AssertionError

    @staticmethod
    def bubbleSort(list_name, list_num):
        """
        冒泡排序
        :param list_name: 传入排序字段名
        :param list_num:  传入字段值

        :return list_name: list_num排序后对应的list_name排序
        :return list_num:  大到小排序好的list_num
        """
        for i in range(len(list_num)):
            for j in range(len(list_num) - i - 1):
                if list_num[j] < list_num[j + 1]:
                    list_num[j], list_num[j + 1] = list_num[j + 1], list_num[j]
                    list_name[j], list_name[j + 1] = list_name[j + 1], list_name[j]
        return list_name, list_num





if __name__ == "__main__":
    url = "https://192.168.111.191:443/api/v1/auth/login"
    name = "yskj"
    password = "yskj2407"
    a = PSPApi()
    b = a.GetCookie(url, name, password)







