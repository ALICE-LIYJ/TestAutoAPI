import unittest
import allure
import os
import pytest
import time
from common.requests_handler import RequestHandler
from common.KeyWord import PSPApi
import requests


url = "https://192.168.111.191:443/api/v1/auth/login"
name = "yskj"
password = "yskj2407"
uid = "a47c6219-ee51-470b-81e6-cb4b1c17cec0"
submituid = "30cd75e1-b1f1-44dd-9daa-8d35e2999b99"
timestamp = time.time()

@allure.epic("PSP")
@allure.feature("系统管理-计算应用")
@allure.story("本地应用模版")

class TestLocalApp(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.severity("blocker")
    @allure.title("添加本地应用模版")
    def test_01AddLocalApp_Success(self):
        """
        添加应用成功
        """

        with allure.step("添加本地应用"):
            print("添加本地应用成功")

        addapp_url = 'https://192.168.111.191:443/api/v1/app/template'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "new_type": "测试starccm本地应用",
            "base_name": "STARCCM+ AUTOTEST-PSP 18.02",
            "bin_path":[{"key":"az-dongfeng","value":"/test/starccm.sim"}],
            "image":"test本地",
            "description": "测试starccm软件1",
            "icon": "https://www.baidu.com/img/bd_logo1.png",
            "base_version": "18.02",
            "new_version": "starccm-test14.04",
            "compute_type": "local",
            "cloud_out_app_id": "4UMmozZCBAh",
       	    "queues": [{"queue_name": "workq","cpu_number": 0,"select": True}],
		    "enable_residual":True,
		    "residual_log_parser":"starccm",
		    "scheduler_param":[{"key": "test123", "value": "/test123"}]
        }

        res = self.req.visit('post',addapp_url,headers=headers,json=body)
        #根据请求结果中的code进行断言
        print(res)
        self.assertEqual(0,res['code'])

    @allure.severity("blocker")
    @allure.title("发布本地应用")
    def test_02PublishLocalApp_Success(self):
        """
        发布应用
        """

        with allure.step("发布应用"):
            print("发布应用成功")

        publishapp_url = 'https://192.168.111.191/api/v1/app/template/publish'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "names": ["测试starccm本地应用 starccm-test14.04"],
	        "state": "published",
	        "compute_type": "local"
        }

        res = self.req.visit('put', publishapp_url, json=body,headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

    @allure.severity("blocker")
    @allure.title("取消发布本地应用")
    def test_03UnPublishLocalApp_Success(self):
        """
        取消发布应用
        """
        with allure.step("取消发布应用"):
            print("取消发布应用成功")

        publishapp_url = 'https://192.168.111.191/api/v1/app/template/publish'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "names": ["测试starccm本地应用 starccm-test14.04"],
	        "state": "unpublished",
	        "compute_type": "local"
        }
        res = self.req.visit('put', publishapp_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

    @allure.severity("blocker")
    @allure.title("删除本地应用")
    def test_04DeleteLocalApp_Success(self):
        """
        删除应用
        """
        with allure.step("删除应用"):
            print("删除应用成功")

        deleteapp_url = 'https://192.168.111.191/api/v1/app/template?name=测试starccm本地应用 starccm-test14.04&compute_type=local'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('delete', deleteapp_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

    @allure.title("添加本地应用时：类型为空")
    def test_05AddLocalApp_NoNewType(self):
        """
        不输入类型
        """
        with allure.step("步骤一：类型为空"):
            pass
        with allure.step("步骤二：添加本地应用失败"):
            print("报错：模版类型不能为空")

        addapp_url = 'https://192.168.111.191:443/api/v1/app/template'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "new_type": "",
            "base_name": "jn-STAR-CCM+ 10.00-R8",
            "bin_path": [{"key": "az-dongfeng", "value": "/test/starccm.sim"}],
            "image": "test本地",
            "description": "测试starccm软件1",
            "icon": "https://www.baidu.com/img/bd_logo1.png",
            "base_version": "10.00-R8",
            "new_version": "starccm-test14.04",
            "compute_type": "local",
            "cloud_out_app_id": "4UMmozZCBAh",
            "queues": [{"queue_name": "workq", "cpu_number": 0, "select": True}],
            "enable_residual": True,
            "residual_log_parser": "starccm",
            "scheduler_param": [{"key": "test123", "value": "/test123"}]
        }
        res = self.req.visit('post', addapp_url, headers=headers, json=body)
        # 根据请求结果中的code进行断言
        print(res)
        self.assertEqual(10002, res['code'])
        self.assertEqual("请求参数错误", res['message'])


    @allure.title("添加本地应用时：版本为空")
    def test_06AddLocalApp_NoNewVersion(self):
        """
        不输入版本
        """
        with allure.step("步骤一：版本为空"):
            pass
        with allure.step("步骤二：添加本地应用失败"):
            print("报错：模版版本不能为空")

        addapp_url = 'https://192.168.111.191:443/api/v1/app/template'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "new_type": "测试本地应用Starccm",
            "base_name": "STARCCM+ AUTOTEST-PSP 18.02",
            "bin_path": [{"key": "az-dongfeng", "value": "/test/starccm.sim"}],
            "image": "test本地",
            "description": "测试starccm软件1",
            "icon": "https://www.baidu.com/img/bd_logo1.png",
            "base_version": "18.02",
            "new_version": "",
            "compute_type": "local",
            "cloud_out_app_id": "4UMmozZCBAh",
            "queues": [{"queue_name": "workq", "cpu_number": 0, "select": True}],
            "enable_residual": True,
            "residual_log_parser": "starccm",
            "scheduler_param": [{"key": "test123", "value": "/test123"}]
        }
        res = self.req.visit('post', addapp_url, headers=headers, json=body)
        # 根据请求结果中的code进行断言
        print(res)
        self.assertEqual(10002, res['code'])
        self.assertEqual("请求参数错误", res['message'])


    @allure.title("添加本地应用时：镜像名和可执行文件路径为空")
    def test_07AddLocalApp_NoImageAndBinPath(self):
        """
        不输入镜像名
        不输入可执行文件路径
        """
        with allure.step("步骤一：镜像名为空"):
            pass
        with allure.step("步骤二：可执行文件路径为空"):
            pass
        with allure.step("步骤三：添加本地应用失败"):
            print("报错：可执行文件路径或者镜像名必须填写一项")

        addapp_url = 'https://192.168.111.191:443/api/v1/app/template'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "new_type": "测试本地应用Starccm",
            "base_name": "STARCCM+ AUTOTEST-PSP 18.02",
            "bin_path":[],
            "image": "",
            "description": "测试starccm软件1",
            "icon": "https://www.baidu.com/img/bd_logo1.png",
            "base_version": "18.02",
            "new_version": "test123",
            "compute_type": "local",
            "cloud_out_app_id": "4UMmozZCBAh",
            "queues": [{"queue_name": "workq", "cpu_number": 0, "select": True}],
            "enable_residual": True,
            "residual_log_parser": "starccm",
            "scheduler_param": [{"key": "test123", "value": "/test123"}]
        }
        res = self.req.visit('post', addapp_url, headers=headers, json=body)
        # 根据请求结果中的code进行断言
        print(res)
        self.assertEqual(11016, res['code'])
        self.assertEqual("添加应用失败", res['message'])


@allure.epic("PSP")
@allure.feature("系统管理-计算应用")
@allure.story("云应用模版")

class TestCloudApp(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.severity("critical")
    @allure.title("发布云应用")
    def test_01PublishCloudApp_Success(self):
        """
        发布云应用
        """
        with allure.step("发布云应用"):
            print("发布云应用成功")

        publishapp_url = 'https://192.168.111.191/api/v1/app/template/publish'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "names":["Code Aster 14.6"],
            "state":"published",
            "compute_type":"cloud"
        }
        res = self.req.visit('put', publishapp_url, json=body, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.severity("critical")
    @allure.title("取消发布云应用")
    def test_02UnPublishCloudApp_Success(self):
        """
        取消发布云应用
        """
        with allure.step("取消发布云应用"):
            print("取消发布云应用成功")

        publishapp_url = 'https://192.168.111.191/api/v1/app/template/publish'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "names":["Code Aster 14.6"],
            "state":"unpublished",
            "compute_type":"cloud"
        }
        res = self.req.visit('put', publishapp_url, json=body, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

@allure.epic("PSP")
@allure.feature("系统管理-作业统计")
@allure.story("应用统计")

class TestAppStatistics(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("应用-统计总览-按照计算类型：“远算云”过滤")
    def test_01SearchCloudAppStatistics_Success(self):
        """
        [应用]-[统计总览]
        按照计算类型：“远算云”过滤查询应用数据
        """
        app_url = 'https://192.168.111.191/api/v1/job/statistics/overview?compute_type=cloud&start_time=1696916816&end_time=1699508816&query_type=app&page_size=10&page_index=1&__timestamp__=1699509391406'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', app_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("cloud",res['data']['overviews'][0]['computeType'])


    @allure.title("应用-统计总览-按照计算类型：“本地”过滤")
    def test_02SearchLocalAppStatistics_Success(self):
        """
        [应用]-[统计总览]
        按照计算类型：“本地”过滤查询应用数据
        """
        app_url = 'https://192.168.111.191/api/v1/job/statistics/overview?compute_type=local&start_time=1696916816&end_time=1699508816&query_type=app&page_size=10&page_index=1&__timestamp__=1699509591626'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', app_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("local",res['data']['overviews'][0]['computeType'])


    @allure.title("应用-统计明细-按照计算类型：“远算云”过滤")
    def test_03SearchCloudAppDetail_Success(self):
        """
        [应用]-[统计明细]
        按照计算类型：“远算云”过滤查询应用数据
        """
        app_url = 'https://192.168.111.191/api/v1/job/statistics/detail?compute_type=cloud&start_time=1696916816&end_time=1699508816&query_type=app&page_size=10&page_index=1&__timestamp__=1699509981224'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', app_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("cloud",res['data']['job_details'][0]['type'])


    @allure.title("应用-统计明细-按照计算类型：“本地”过滤")
    def test_04SearchLocalAppDetail_Success(self):
        """
        [应用]-[统计明细]
        按照计算类型：“本地”过滤查询应用数据
        """
        app_url = 'https://192.168.111.191/api/v1/job/statistics/detail?compute_type=local&start_time=1696916816&end_time=1699508816&query_type=app&page_size=10&page_index=1&__timestamp__=1699510199985'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', app_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("local",res['data']['job_details'][0]['type'])


@allure.epic("PSP")
@allure.feature("系统管理-作业统计")
@allure.story("用户统计")

class TestUserStatistics(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("用户-统计总览-按照计算类型：“远算云”过滤")
    def test_01SearchCloudUserStatistics_Success(self):
        """
        [用户]-[统计总览]
        按照计算类型：“远算云”过滤查询用户数据
        """
        user_url = 'https://192.168.111.191/api/v1/job/statistics/overview?compute_type=cloud&start_time=1696918508&end_time=1699510508&query_type=user&page_size=10&page_index=1&__timestamp__=1699510521657'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', user_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("cloud",res['data']['overviews'][0]['computeType'])


    @allure.title("用户-统计总览-按照计算类型：“本地”过滤")
    def test_02SearchLocalUserStatistics_Success(self):
        """
        [用户]-[统计总览]
        按照计算类型：“本地”过滤查询用户数据
        """
        user_url = 'https://192.168.111.191/api/v1/job/statistics/overview?compute_type=local&start_time=1696918508&end_time=1699510508&query_type=user&page_size=10&page_index=1&__timestamp__=1699510618798'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', user_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("local",res['data']['overviews'][0]['computeType'])


    @allure.title("用户-统计明细-按照计算类型：“远算云”过滤")
    def test_03SearchCloudUserDetail_Success(self):
        """
        [用户]-[统计明细]
        按照计算类型：“远算云”、用户名称：“yskj” 过滤查询用户数据
        """
        user_url = 'https://192.168.111.191/api/v1/job/statistics/detail?compute_type=cloud&start_time=1696918508&end_time=1699510508&names=yskj&query_type=user&page_size=10&page_index=1&__timestamp__=1699510704073'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', user_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("cloud",res['data']['job_details'][0]['type'])
        self.assertEqual("yskj",res['data']['job_details'][0]['user_name'])


    @allure.title("用户-统计明细-按照计算类型、用户名称过滤")
    def test_04SearchLocalUserDetail_Success(self):
        """
        [用户]-[统计明细]
        按照计算类型：“本地”、用户名称：“yskj” 过滤查询应用数据
        """
        user_url = 'https://192.168.111.191/api/v1/job/statistics/detail?compute_type=local&start_time=1696918508&end_time=1699510508&names=yskj&query_type=user&page_size=10&page_index=1&__timestamp__=1699510826016'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', user_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("local",res['data']['job_details'][0]['type'])
        self.assertEqual("yskj",res['data']['job_details'][0]['user_name'])



@allure.epic("PSP")
@allure.feature("系统管理-账单管理")
@allure.story("作业账单")

class TestJobBillings(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("按照“用户名称”过滤")
    def test_01SearchUsername_Success(self):
        """
        按照用户名称：“yskj”过滤查询账单数据
        """
        account_url = 'https://192.168.111.191/api/v1/billing/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
                "filter": {
		            "user_name": "yskj",
		            "resource_id": "",
		            "merchandise_ids": [],
		            "job_submit_start_time": 1697265661,
		            "job_submit_end_time": 1699857661
	            },
	            "page": {
		            "index": 1,
		            "size": 10
	            }
        }

        res = self.req.visit('post', account_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("yskj",res['data']['billings'][0]['user_name'])


    @allure.title("按照“作业编号”过滤")
    def test_02SearchJobID_Success(self):
        """
        按照作业编号：“4ZsWyGdax39”过滤查询账单数据
        """
        account_url = 'https://192.168.111.191/api/v1/billing/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
                "filter": {
		            "user_name": "",
		            "resource_id": "4ZsWyGdax39",
		            "merchandise_ids": [],
		            "job_submit_start_time": 1697265661,
		            "job_submit_end_time": 1699857661
	            },
	            "page": {
		            "index": 1,
		            "size": 10
	            }
        }

        res = self.req.visit('post', account_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4ZsWJX7xR15",res['data']['billings'][0]['id']) #账单编号
        self.assertEqual("4ZsWyGdax39",res['data']['billings'][0]['resource_id']) #作业编号


    @allure.title("按照“应用名称”过滤")
    def test_03SearchMerchandiseName_Success(self):
        """
        按照应用名称："Fluent v22R2" --4ZLj2MH2moC 过滤查询账单数据
        """
        account_url = 'https://192.168.111.191/api/v1/billing/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
                "filter": {
		            "user_name": "",
		            "resource_id": "",
		            "merchandise_ids": ["4ZLj2MH2moC"],
		            "job_submit_start_time": 1698738618,
		            "job_submit_end_time": 1701243798
	            },
	            "page": {
		            "index": 1,
		            "size": 10
	            }
        }

        res = self.req.visit('post', account_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Fluent v22R2",res['data']['billings'][0]['merchandise_name']) #应用名称



@allure.epic("PSP")
@allure.feature("系统管理-报表管理")
@allure.story("报表统计")

class TestReport(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("CPU平均利用率")
    def test_01CPU_UT_AVG(self):
        """
        CPU平均利用率
        """
        with allure.step("步骤一：查询24小时的CPU平均利用率"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/resourceUtAvg?type=CPU_UT_AVG&start=1700624396018&end=1700710796018&__timestamp__=1700710796167'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("内存平均利用率")
    def test_02MEM_UT_AVG(self):
        """
        内存平均利用率
        """
        with allure.step("步骤一：查询7天内的内存平均利用率"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/resourceUtAvg?type=MEM_UT_AVG&start=1700111548913&end=1700716348913&__timestamp__=1700716349011'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("磁盘吞吐率")
    def test_03TOTAL_IO_UT_AVG(self):
        """
        磁盘吞吐率
        """
        with allure.step("步骤一：查询7天内的磁盘吞吐率"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/resourceUtAvg?type=TOTAL_IO_UT_AVG&start=1700111548913&end=1700716348913&__timestamp__=1700716514678'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("磁盘使用情况")
    def test_04DISK_UT_AVG(self):
        """
        磁盘使用情况
        """
        with allure.step("步骤一：查询24小时内的磁盘使用情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/diskUtAvg?type=DISK_UT_AVG&start=1700630214282&end=1700716614282&__timestamp__=1700716614380'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("核时使用情况")
    def test_05CPU_TIME_SUM(self):
        """
        核时使用情况
        """
        with allure.step("步骤一：查询30天内的核时使用情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/cpuTimeSum?type=CPU_TIME_SUM&start=1698124768677&end=1700716768677&__timestamp__=1700716768779'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("作业投递数情况")
    def test_06JOB_COUNT(self):
        """
        作业投递数情况
        """
        with allure.step("步骤一：查询30天内的作业投递数情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/jobCount?type=JOB_COUNT&start=1698124768677&end=1700716768677&__timestamp__=1700716929006'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("用户数与作业数情况")
    def test_07JOB_DELIVER_COUNT(self):
        """
        用户数与作业数情况
        """
        with allure.step("步骤一：查询30天内的用户数与作业数情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/jobDeliverCount?type=JOB_DELIVER_COUNT&start=1698124768677&end=1700716768677&__timestamp__=1700717010849'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("作业等待情况")
    def test_08JOB_WAIT_STATISTIC(self):
        """
        作业等待情况
        """
        with allure.step("步骤一：查询24小时内的作业等待情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/jobWaitStatistic?type=JOB_WAIT_STATISTIC&start=1700630712348&end=1700717112349&__timestamp__=1700717112462'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])


    @allure.title("许可证软件使用情况")
    def test_09LICENSE_APP_USED_UT_AVG(self):
        """
        许可证软件使用情况
        """
        with allure.step("步骤一：查询24小时内许可证软件使用情况"):
            pass

        report_url = 'https://192.168.111.191/api/v1/report/licenseAppUsedUtAvg?type=LICENSE_APP_USED_UT_AVG&start=1700630712348&end=1700717112349&__timestamp__=1700717215487'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        res = self.req.visit('get', report_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])



@allure.epic("PSP")
@allure.feature("系统管理-许可证管理")

class TestLicenseManage(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("许可证管理")
    def test_01ADD_Licnese_Success(self):
        """
        添加许可证
        """
        with allure.step("步骤一：添加许可证"):
            print("添加许可证成功")

        license_url = 'https://192.168.111.191/api/v1/licenseManagers'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "app_type": "PSP_AUTO_LICENSE_001",
            "os": 1,
            "desc": "PSP自动化脚本测试许可证",
            "compute_rule": "echo 1\nsleep 1\n"
        }
        res = self.req.visit('post', license_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True,res['success'])

        managerID = res['data']['id']
        print(managerID)

        with allure.step("步骤二：列出许可证信息"):
            print("列出许可证信息成功")

        license_url = 'https://192.168.111.191/api/v1/licenseManagers/{}?__timestamp__={}'.format(managerID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', license_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True, res['success'])
        self.assertEqual("PSP_AUTO_LICENSE_001",res['data']['app_type'])
        self.assertEqual("PSP自动化脚本测试许可证",res['data']['desc'])

        with allure.step("步骤三：编辑许可证信息"):
            print("编辑许可证信息成功")

        license_url = 'https://192.168.111.191/api/v1/licenseManagers/{}'.format(managerID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "id": managerID,
            "app_type": "PSP_AUTO_LICENSE_UPDATE",
            "os": 1,
            "desc": "PSP自动化脚本测试许可证",
            "compute_rule": "echo 1\nsleep 1\nmkdir /test\ncd /test\n"
        }
        res = self.req.visit('put', license_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True, res['success'])

        time.sleep(1)
        with allure.step("步骤四：列出修改后的许可证信息"):
            print("列出修改后的许可证信息成功")

        license_url = 'https://192.168.111.191/api/v1/licenseManagers/{}?__timestamp__={}'.format(managerID, timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', license_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True, res['success'])
        self.assertEqual("PSP_AUTO_LICENSE_UPDATE", res['data']['app_type'])
        self.assertEqual("echo 1\nsleep 1\nmkdir /test\ncd /test\n", res['data']['compute_rule'])

        with allure.step("步骤五：添加许可证服务器"):
            print("添加许可证服务器成功")
        license_url = 'https://192.168.111.191/api/v1/licenseInfos'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "license_name": "test1",
            "license_env_var": "test1",
            "mac_addr": "00:00:00:00:00:00",
            "license_url": "115.159.149.167",
            "port": 1001,
            "license_num": "4E30 AFEF CB5D D27D 353F 5B3D 7D",
            "allowable_hpc_endpoints": ["http://10.0.10.2:8080"],
            "weight": 9,
            "auth": True,
            "collector_type": "altair",
            "tool_path": "/home/yuansuan/lic_tool/lmutil",
            "start_time": "2023-11-22 13:59:24",
            "end_time": "2023-11-24 19:00:00",
            "manager_id": managerID
        }
        res = self.req.visit('post', license_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True, res['success'])

        #返回许可证服务器id
        licenseID = res['data']['id']
        print(licenseID)

        with allure.step("步骤六：添加同名的许可证服务器"):
            print("添加许可证服务器失败")
        license_url = 'https://192.168.111.191/api/v1/licenseInfos'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "license_name": "test1",
            "license_env_var": "test1",
            "mac_addr": "00:00:00:00:00:00",
            "license_url": "115.159.149.167",
            "port": 1001,
            "license_num": "4E30 AFEF CB5D D27D 353F 5B3D 7D",
            "allowable_hpc_endpoints": ["http://10.0.10.2:8080"],
            "weight": 9,
            "auth": True,
            "collector_type": "altair",
            "tool_path": "/home/yuansuan/lic_tool/lmutil",
            "start_time": "2023-11-22 13:59:24",
            "end_time": "2023-11-24 19:00:00",
            "manager_id": managerID
        }
        res = self.req.visit('post', license_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(22013, res['code'])
        self.assertEqual(False, res['success'])
        self.assertEqual("许可证名字重复", res['message'])


        with allure.step("步骤七：许可证服务器下添加模块"):
            print("添加模块成功")

        module_url = 'https://192.168.111.191/api/v1/moduleConfigs'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "license_id": licenseID,
	        "module_name": "moduleA",
	        "total": 2
        }
        body1 = {
            "license_id": licenseID,
            "module_name": "moduleB",
            "total": 2
        }
        res = self.req.visit('post', module_url, headers=headers,json=body)
        res1 = self.req.visit('post', module_url, headers=headers,json=body1)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(True, res1['success'])

        with allure.step("步骤八：许可证服务器下添加同名模块"):
            print("添加模块失败")

        module_url = 'https://192.168.111.191/api/v1/moduleConfigs'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "license_id": licenseID,
            "module_name": "moduleA",
            "total": 2
        }
        res = self.req.visit('post', module_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(22016, res['code'])
        self.assertEqual("许可证模块名字重复", res['message'])


        with allure.step("步骤九：列出模块数量详情"):
            print("列出模块数量详情成功")

        module_url = 'https://192.168.111.191/api/v1/licenseInfos/{}/moduleConfigs?__timestamp__={}'.format(licenseID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("moduleA", res['data']['module_config_infos'][0]['module_name'])
        self.assertEqual("moduleB", res['data']['module_config_infos'][1]['module_name'])

        moduleA_ID = res['data']['module_config_infos'][0]['id']
        print(moduleA_ID)

        moduleB_ID = res['data']['module_config_infos'][1]['id']
        print(moduleB_ID)


        with allure.step("步骤十：更新修改模块数量详情"):
            print("更新修改模块数量详情成功")

        module_url = 'https://192.168.111.191/api/v1/moduleConfigs/{}'.format(moduleA_ID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "id": moduleA_ID,
            "license_id": licenseID,
            "module_name": "moduleA_1",
            "total": 3
        }
        res = self.req.visit('put', module_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        module_url = 'https://192.168.111.191/api/v1/moduleConfigs/{}'.format(moduleB_ID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "id": moduleB_ID,
            "license_id": licenseID,
            "module_name": "moduleB_1",
            "total": 6
        }
        res = self.req.visit('put', module_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        time.sleep(1)

        with allure.step("步骤十一：列出更新后的模块数量详情"):
            print("列出更新后的模块数量详情成功")

        module_url = 'https://192.168.111.191/api/v1/licenseInfos/{}/moduleConfigs?__timestamp__={}'.format(licenseID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("moduleA_1", res['data']['module_config_infos'][0]['module_name'])
        self.assertEqual(3, res['data']['module_config_infos'][0]['total'])

        self.assertEqual("moduleB_1", res['data']['module_config_infos'][1]['module_name'])
        self.assertEqual(6, res['data']['module_config_infos'][1]['total'])


        with allure.step("步骤十二：删除模块"):
            print("删除模块成功")

        module_url = 'https://192.168.111.191/api/v1/moduleConfigs/{}'.format(moduleB_ID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('delete', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


        with allure.step("步骤十三：列出删除后的模块数量详情"):
            print("列出删除后的模块数量详情成功")

        module_url = 'https://192.168.111.191/api/v1/licenseInfos/{}/moduleConfigs?__timestamp__={}'.format(licenseID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("moduleA_1", res['data']['module_config_infos'][0]['module_name'])
        self.assertEqual(3, res['data']['module_config_infos'][0]['total'])

        with allure.step("步骤十四：查看许可证模块使用情况报表"):
            print("查看许可证模块使用情况报表成功")

        module_url = 'https://192.168.111.191/api/v1/report/licenseAppModuleUsedUtAvg?license_id={}&license_type=PSP_AUTO_LICENSE_UPDATE&type=LICENSE_APP_MODULE_USED_UT_AVG&start=1700116954010&end=1700721754011&__timestamp__={}'.format(licenseID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("moduleA_1", res['data']['license_app_module_ut_avg'][0]['n'])

        with allure.step("步骤十五：删除许可证服务器"):
            print("删除许可证服务器成功")

        module_url = 'https://192.168.111.191/api/v1/licenseInfos/{}'.format(licenseID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('delete', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        with allure.step("步骤十六：删除许可证"):
            print("删除许可证服务器成功")

        module_url = 'https://192.168.111.191/api/v1/licenseManagers/{}'.format(managerID)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('delete', module_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


@allure.epic("PSP")
@allure.feature("文件管理")
@allure.severity(allure.severity_level.CRITICAL)
class TestFileManagement(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("新建文件夹")
    def test_01CreateDir_Success(self):
        """
        新建文件夹：/test-mkdir
        """
        createdir_url = 'https://192.168.111.191/api/v1/storage/createDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "path": "/test-mkdir",
	        "cross": False,
	        "is_cloud": False,
	        "user_name": "yskj"
        }
        res = self.req.visit('post', createdir_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("上传文件")
    def test_02UploadFile_Success(self):
        """
        上传文件：/test-mkdir/bluntbody.sim
        """

        with allure.step("步骤一：上传文件前准备"):
            pass
        with allure.step("步骤二：上传文件"):
            pass
        with allure.step("步骤三：分片上传"):
            pass
        with allure.step("步骤四：文件上传成功"):
            pass

        preupload_url = 'https://192.168.111.191/api/v1/storage/preUpload'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "directory": False,
            "_uid": uid,
            "dir": "/./test-mkdir",
            "user_name": "yskj",
            "path": "./test-mkdir/bluntbody.sim",
            "file_size": 4169521
        }
        res = self.req.visit('post', preupload_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        uploadID =  res['data']['upload_id']
        print(uploadID)


        import mimetypes
        from codecs import encode

        dataList = []
        boundary = 'WebKitFormBoundaryfrEtrgDTa0uqpEKU'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=slice; filename={0}'.format('bluntbody.sim')))

        fileType = mimetypes.guess_type('')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('D:\SoftWare\Pycharm\PyCharm Community Edition 2023.2.2\pythonProject\TestData\\bluntbody.sim', 'rb') as f:
            dataList.append(f.read())

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=user_name;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("yskj"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=directory;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=dir;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("/./test-mkdir"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=_uid;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(uid))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=upload_id;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(uploadID))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=path;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("./test-mkdir/bluntbody.sim"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("4169521"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=offset;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=slice_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("4169521"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=finish;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("1"))

        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
            'Cookie':PSPApi.GetCookie(url,name,password)
        }
        upload_url = "https://192.168.111.191/api/v1/storage/upload"
        response = requests.post(upload_url, headers=headers, data=payload, verify=False)
        print(response.text)

        #查看文件详情
        list_url = 'https://192.168.111.191/api/v1/storage/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password),
            "Accept-Encoding": "gzip,deflate,br"
        }
        body = {
            "path": "./test-mkdir",
	        "cross": False,
	        "is_cloud": False,
	        "user_name": "yskj",
	        "filter_regexp_list": [],
	        "show_hide_file": False
        }
        res = requests.post(list_url, headers=headers, json=body)
        print(res)
        self.assertEqual(0,res['code'])
        self.assertEqual(4169521,res['data'][0]['size'])


    @allure.title("下载文件")
    def test_03DownloadFile_Success(self):
        """
       下载文件：/test-mkdir/bluntbody.sim
        """
        download_url = 'https://192.168.111.191/api/v1/storage/batchDownload?file_paths=./test-mkdir/bluntbody.sim&file_name=bluntbody.sim&cross=False&is_cloud=False&is_compress=False&user_name=yskj'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password),
            "Accept-Encoding": "gzip,deflate,br"
        }
        res = requests.get(download_url, headers=headers,verify=False)
        print(res.text)


    @allure.title("文件覆盖")
    def test_04OverWriteFile_Success(self):
        """
        home目录下新建文件夹/test-mkdir，在文件夹/test-mkdir下上传文件bluntbody.sim(3.98MB)，
        后续继续在此文件夹下上传同名的文件bluntbody.sim(0B)，
        选择覆盖选中，
        预期：上传成功，文件展示为bluntbody.sim(0B)
        """
        remove_url = 'https://192.168.111.191/api/v1/storage/remove'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "paths": ["/test-mkdir/bluntbody.sim"],
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', remove_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        preupload_url = 'https://192.168.111.191/api/v1/storage/preUpload'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "directory": False,
            "_uid": uid,
            "dir": "/./test-mkdir",
            "user_name": "yskj",
            "path": "./test-mkdir/bluntbody.sim",
            "file_size": 0
        }
        res = self.req.visit('post', preupload_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        uploadID =  res['data']['upload_id']
        print(uploadID)


        import mimetypes
        from codecs import encode

        dataList = []
        boundary = 'WebKitFormBoundarymrrvpbkz5vVDocav'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=slice; filename={0}'.format('bluntbody.sim')))

        fileType = mimetypes.guess_type('')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('D:\SoftWare\Pycharm\PyCharm Community Edition 2023.2.2\pythonProject\TestOverWrite\\bluntbody.sim', 'rb') as f:
            dataList.append(f.read())

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=user_name;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("yskj"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=directory;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=dir;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("/./test-mkdir"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=_uid;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(uid))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=upload_id;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(uploadID))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=path;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("./test-mkdir/bluntbody.sim"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=offset;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=slice_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=finish;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("1"))

        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
            'Cookie':PSPApi.GetCookie(url,name,password)
        }
        upload_url = "https://192.168.111.191/api/v1/storage/upload"
        response = requests.post(upload_url, headers=headers, data=payload, verify=False)
        print(response.text)

        list_url = 'https://192.168.111.191/api/v1/storage/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "path":"./test-mkdir",
            "cross":False,
            "is_cloud":False,
            "user_name":"yskj",
            "filter_regexp_list":[],
            "show_hide_file":False
        }
        res = self.req.visit('post', list_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual(0,res['data'][0]['size'])
        self.assertEqual("test-mkdir/bluntbody.sim",res['data'][0]['path'])


    @allure.title("删除文件")
    def test_05RemoveFile_Success(self):
        """
        删除文件：/test-mkdir/bluntbody.sim
        """
        remove_url = 'https://192.168.111.191/api/v1/storage/remove'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "paths": ["/test-mkdir/bluntbody.sim"],
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', remove_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("文件夹重命名")
    def test_06RenameDir_Success(self):
        """
        文件夹重命名：/test-mkdir 重命名为：/test-rm
        """
        rename_url = 'https://192.168.111.191/api/v1/storage/rename'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "path":"/test-mkdir",
            "newpath":"/test-rm",
            "user_name":"yskj",
            "cross":False,
            "is_cloud":False
        }
        res = self.req.visit('put', rename_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("移动场景测试：将文件夹从第二层级移动到第一层级")
    def test_07MoveDir_Success(self):

        with allure.step("步骤一：新建文件夹：/test-rm/test111"):
            pass
        create_url = 'https://192.168.111.191/api/v1/storage/createDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "path": "./test-rm/test111",
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', create_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        with allure.step("步骤二：移动文件夹：/home/test-rm/test111 移动到home目录下"):
            pass
        move_url = 'https://192.168.111.191/api/v1/storage/move'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "src_paths": ["./test-rm/test111"],
            "dst_path": ".",
            "cross": False,
            "is_cloud": False,
            "overwrite": True,
            "user_name": "yskj"
        }
        res = self.req.visit('put', move_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("移动场景测试：文件夹移动到源路径")
    def test_08MoveDir_Failed(self):
        """
        移动文件夹：/home/test-rm/ 移动到/home/test-rm
        """
        move_url = 'https://192.168.111.191/api/v1/storage/move'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "src_paths":["./test-rm"],
            "dst_path":".",
            "cross":False,
            "is_cloud":False,
            "overwrite":True,
            "user_name":"yskj"
        }
        res = self.req.visit('put', move_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(15019, res['code'])
        self.assertEqual("目标路径不能与源文件路径一致", res['message'])


    @allure.title("删除文件夹")
    def test_10DeleteDir_Success(self):
        """
        删除文件夹：/home/test111
        删除文件夹：/home/test-rm
        """
        remove_url = 'https://192.168.111.191/api/v1/storage/remove'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "paths": ["/test111"],
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        body1 = {
            "paths": ["/test-rm"],
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', remove_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        res1 = self.req.visit('post', remove_url, headers=headers, json=body1)
        print(res1)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res1['code'])


    @allure.title("移动场景测试：相同文件夹名称，文件夹从第三层级移动到第二层级")
    def test_11MoveCase_Success(self):
        """
        home目录下新建文件夹/LYJ123/LYJ123/LYJ123，
        将文件夹/LYJ123/LYJ123/移动到第二层级，
        选择覆盖选中，
        预期：移动失败，提示：目标路径不能与源文件路径一致
        """
        with allure.step("步骤一：新建文件夹层级：/LYJ123/LYJ123/LYJ123"):
            pass

        create_url = 'https://192.168.111.191/api/v1/storage/createDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "path": "./LYJ123/LYJ123/LYJ123",
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', create_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        with allure.step("步骤二：移动文件夹到第二层级：/LYJ123/LYJ123"):
            pass
        with allure.step("步骤三：覆盖选中，移动失败，报错：目标路径不能与源文件路径一致"):
            pass

        move_url = 'https://192.168.111.191/api/v1/storage/move'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "src_paths":["./LYJ123/LYJ123/LYJ123"],
            "dst_path":"./LYJ123/LYJ123",
            "cross":False,
            "is_cloud":False,
            "overwrite":True,
            "user_name":"yskj"
        }
        res = self.req.visit('put', move_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(15019, res['code'])
        self.assertEqual("目标路径不能与源文件路径一致", res['message'])

        with allure.step("步骤四：删除文件夹/LYJ123"):
            pass

        remove_url = 'https://192.168.111.191/api/v1/storage/remove'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "paths":["/LYJ123"],
            "cross":False,
            "is_cloud":False,
            "user_name":"yskj"
        }
        res = self.req.visit('post', remove_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("移动场景测试：相同文件夹名称，文件夹从第三层级移动到第一层级")
    def test_12MoveCase1_Success(self):
        """
        home目录下新建文件夹/LYJ111/LYJ111/LYJ111，
        将文件夹/LYJ111移动到第一层级，
        选择覆盖选中，
        预期：移动失败，提示：不能覆盖文件的父目录
        """
        with allure.step("步骤一：新建文件夹层级：/LYJ123/LYJ123/LYJ123"):
            pass

        create_url = 'https://192.168.111.191/api/v1/storage/createDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "path": "./LYJ111/LYJ111/LYJ111",
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj"
        }
        res = self.req.visit('post', create_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        with allure.step("步骤二：移动文件夹到第一层级：/LYJ111"):
            pass
        with allure.step("步骤三：覆盖选中，移动失败，报错：不能覆盖文件的父目录"):
            pass

        move_url = 'https://192.168.111.191/api/v1/storage/move'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "src_paths":["./LYJ111/LYJ111/LYJ111"],
            "dst_path":"./LYJ111",
            "cross":False,
            "is_cloud":False,
            "overwrite":True,
            "user_name":"yskj"
        }
        res = self.req.visit('put', move_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(15056, res['code'])
        self.assertEqual("不能覆盖文件的父目录", res['message'])

        with allure.step("步骤四：删除文件夹/LYJ111"):
            pass

        remove_url = 'https://192.168.111.191/api/v1/storage/remove'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "paths":["/LYJ111"],
            "cross":False,
            "is_cloud":False,
            "user_name":"yskj"
        }
        res = self.req.visit('post', remove_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


    @allure.title("分享文件")
    def test_13ShareFile_Success(self):
        """
        分享文件
        /test-submit(请勿删除！！！)/Blade.sim文件
        用户：yskj 分享给 用户：tina1
        """
        with allure.step("步骤一：分享文件"):
            pass

        share_url = 'https://192.168.111.191/api/v1/storage/share/send'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "share_file_path": "./test-submit(请勿删除！！！)/Blade.sim",
            "share_type": 2,
            "share_user_list": ["51cMjxitbKS"]
        }
        res = self.req.visit('post', share_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


        with allure.step("步骤二：查看用户日志"):
            pass

        send_url = 'https://192.168.111.191/api/v1/auditlog/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "page": {
                "index": 1,
                "size": 10
            },
            "operate_type": 1,
            "user_name": "",
            "ip_address": "",
            "start_time": "",
            "end_time": ""
        }
        res = self.req.visit('post', send_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("用户yskj分享文件[./test-submit(请勿删除！！！)/Blade.sim]给[tina1]",res['data']['list'][0]['operate_content'])
        self.assertEqual("yskj",res['data']['list'][0]['user_name'])


    @allure.title("发送文件")
    def test_14SendFile_Success(self):
        """
        发送文件
        /test-submit(请勿删除！！！)/Blade.sim文件
        用户：yskj 发送给 用户：jimmy
        """
        with allure.step("步骤一：分享文件"):
            pass

        send_url = 'https://192.168.111.191/api/v1/storage/share/send'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "share_file_path": "./test-submit(请勿删除！！！)/STARCCM_test_Blade.sim",
	        "share_type": 1,
	        "share_user_list": ["516UqsKdCVw"]
        }
        res = self.req.visit('post', send_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


        with allure.step("步骤二：查看用户日志"):
            pass

        send_url = 'https://192.168.111.191/api/v1/auditlog/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "page": {
                "index": 1,
                "size": 10
            },
            "operate_type": 1,
            "user_name": "",
            "ip_address": "",
            "start_time": "",
            "end_time": ""
        }
        res = self.req.visit('post', send_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("用户yskj发送文件[./test-submit(请勿删除！！！)/STARCCM_test_Blade.sim]给[jimmy]",res['data']['list'][0]['operate_content'])
        self.assertEqual("yskj",res['data']['list'][0]['user_name'])


@allure.epic("PSP")
@allure.feature("作业管理")
@allure.story("查询功能")

class TestJobManagement(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()


    @allure.title("按照“作业编号”过滤")
    def test_01SearchJobID_Success(self):
        """
        按照作业编号查询数据
        输入作业编号：4X5sj5So6hu
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "4X5sj5So6hu",
		        "job_name": "",
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4X5sj5So6hu", res['data']['jobs'][0]['id'])


    @allure.title("按照“作业名称”过滤")
    def test_02SearchJobName_Success(self):
        """
        按照作业名称查询数据
        输入作业名称：test1
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "test1",
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        #self.assertEqual("test1", res['data']['jobs'][0]['name'])


    @allure.title("按照“用户名称”过滤")
    def test_03SearchUserName_Success(self):
        """
        按照用户名称查询数据
        选择用户名称：yskj
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "",
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "user_names": ["yskj"]
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("yskj", res['data']['jobs'][0]['user_name'])


    @allure.title("按照“应用名称”过滤")
    def test_04SearchAppName_Success(self):
        """
        按照应用名称查询数据
        选择应用名称：jn-STAR-CCM+ 14.02
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "page": {
                "index": 1,
                "size": 10
            },
            "filter": {
                "job_id": "",
                "job_name": "",
                "app_names": ["jn-STAR-CCM+ 14.02"],
                "states": [],
                "queues": [],
                "user_names": []
            }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("jn-STAR-CCM+ 14.02", res['data']['jobs'][0]['app_name'])


    @allure.title("按照“队列名称”过滤")
    def test_05SearchQueueName_Success(self):
        """
        按照队列名称查询数据
        选择队列名称：cloud
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "",
		        "app_names": [],
		        "states": [],
		        "queues": ["cloud"],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("cloud", res['data']['jobs'][0]['queue'])


    @allure.title("按照“计算状态”过滤")
    def test_06SearchJobState_Success(self):
        """
        按照计算状态查询数据
        选择计算状态：已完成
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "",
		        "app_names": [],
		        "states": ["Completed"],
		        "queues": [],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Completed", res['data']['jobs'][0]['state'])


    @allure.title("按照“作业类型”过滤")
    def test_07SearchJobType_Success(self):
        """
        按照作业类型查询数据
        选择作业类型：本地
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "",
		        "app_names": [],
                "job_types":["local"],
		        "states": [],
		        "queues": [],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("local", res['data']['jobs'][0]['type'])


    @allure.title("按照“计算状态、作业名称、队列名称”组合过滤")
    def test_08UnionSearchJobSuccess(self):
        """
        组合查询
        选择计算状态：已终止
        选择作业名称：test
        选择队列名称：test
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "job_id": "",
		        "job_name": "test",
		        "app_names": [],
		        "states": ["Terminated"],
		        "queues": ["test"],
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Terminated", res['data']['jobs'][0]['state'])
        self.assertEqual("test", res['data']['jobs'][0]['queue'])


    @allure.title("按照“作业名称、应用名称、作业类型”组合过滤")
    def test_09UnionSearchJobSuccess(self):
        """
        组合查询
        选择作业名称：STAR
        选择作业类型：远算云
        选择应用名称：Code Aster 14.6
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "page": {
                "index": 1,
                "size": 10
            },
            "filter": {
                "job_id": "",
                "job_name": "STAR",
                "app_names": ["Code Aster 14.6"],
                "job_types":["cloud"],
                "states": [],
                "queues": [],
                "user_names": []
            }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Code Aster 14.6", res['data']['jobs'][0]['app_name'])
        self.assertEqual("cloud", res['data']['jobs'][0]['type'])


    @allure.title("点击作业编号查看作业详情")
    def test_10JobIDToDetail_Success(self):
        """
        点击作业编号跳转到作业详情界面
        作业编号：516QfP3Ai2j
        """
        job_url = 'https://192.168.111.191/api/v1/job/detail?job_id=516QfP3Ai2j&__timestamp__={}'.format(timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }

        res = self.req.visit('get', job_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4ZR3n7tUN8A", res['data']['app_id'])
        self.assertEqual("jn2-STAR-CCM+ 10.02-R8.liuqi", res['data']['app_name'])
        self.assertEqual("516QfP3Ai2j", res['data']['id'])


    @allure.title("点击作业名称查看作业详情")
    def test_11JobNameToDetail_Success(self):
        """
        点击作业名称跳转到作业详情界面
        作业编号：516LNDGfeKw
        作业名称：test23_Blade_test
        """
        job_url = 'https://192.168.111.191/api/v1/job/detail?job_id=516LNDGfeKw&__timestamp__={}'.format(timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }

        res = self.req.visit('get', job_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("test23_Blade_test", res['data']['name'])
        self.assertEqual("516LNDGfeKw", res['data']['id'])


@allure.epic("PSP")
@allure.feature("作业提交")
@allure.severity(allure.severity_level.BLOCKER)
class TestJobSubmit(unittest.TestCase):

    def setUp(self):
        # 请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()

    @allure.title("本地作业单个提交")
    def test_01LocalJobSubmit_Success(self):
        """
        设置主文件--本地上传bluntbody.sim
        参数配置
        本地作业提交
        """
        with allure.step("步骤一:选择应用"):
            pass
        with allure.step("步骤二:本地上传文件"):
            pass
        with allure.step("步骤三:设置主文件"):
            pass
        with allure.step("步骤四：配置参数"):
            pass
        with allure.step("步骤五：点击提交按钮，确认提交"):
            print("作业提交成功，界面跳转到作业管理界面")
        with allure.step("步骤六：查看作业详情"):
            pass

        createtempdir_url = 'https://192.168.111.191/api/v1/job/createTempDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "compute_type": "local"
        }
        res = self.req.visit('post', createtempdir_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        path = res['data']['path']
        print(path)


        preupload_url = 'https://192.168.111.191/api/v1/storage/preUpload'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "directory": False,
            "_uid": submituid,
            "dir": "",
            "user_name": "yskj",
            "is_cloud": False,
            "tempDirPath": path,
            "cross": True,
            "path": path+"/Testbluntbody.sim",
            "file_size": 4169521
        }
        res = self.req.visit('post', preupload_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        uploadID = res['data']['upload_id']
        print(uploadID)

        import mimetypes
        from codecs import encode

        dataList = []
        boundary = 'WebKitFormBoundary4F3wvse2VGAN0rM9'
        dataList.append(encode('--' + boundary))
        dataList.append(encode(
            'Content-Disposition: form-data; name=slice; filename={0}'.format('Testbluntbody.sim')))

        fileType = mimetypes.guess_type('')[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open('D:\SoftWare\Pycharm\PyCharm Community Edition 2023.2.2\pythonProject\TestData\Testbluntbody.sim',
                  'rb') as f:
            dataList.append(f.read())

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=directory;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=_uid;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(submituid))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=dir;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(""))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=user_name;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("yskj"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=is_cloud;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=tempDirPath;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(path))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=cross;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("1"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=path;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(path+"/Testbluntbody.sim"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("4169521"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=upload_id;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(uploadID))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=offset;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("4169521"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=slice_size;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("0"))

        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=finish;'))
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode("1"))

        dataList.append(encode('--' + boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
            'Cookie': PSPApi.GetCookie(url, name, password),
            'Accept-Encoding': 'gzip,deflate,br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        upload_url = "https://192.168.111.191/api/v1/storage/upload"
        response = requests.post(upload_url, headers=headers, data=payload,verify=False)
        print(response.text)

        time.sleep(1)

        submit_url = 'https://192.168.111.191/api/v1/job/submit'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "app_id":"4ZR3n7tUN8A",
            "main_files":["Testbluntbody.sim"],
            "queue_name":"",
            "work_dir":{"path":path,"is_temp":True},
            "fields":[{"id":"JOB_NAME","value":"test-local","values":[],"type":"text"},
                      {"id":"CPU_NUM","value":"1","values":[],"type":"text"}]
        }
        res = self.req.visit('post', submit_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        time.sleep(3)

        #查询生成的作业情况

        """
        应用：jn2-STAR-CCM+ 10.02-R8.liuqi
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "job_types": [],
		        "start_time": None,
		        "end_time": None,
		        "job_id": "",
		        "job_name": "",
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4ZR3n7tUN8A", res['data']['jobs'][0]['app_id'])
        self.assertEqual("test-local", res['data']['jobs'][0]['name'])
        self.assertEqual("local", res['data']['jobs'][0]['type'])
        self.assertEqual("1", res['data']['jobs'][0]['cpus_alloc'])
        self.assertEqual("workq", res['data']['jobs'][0]['queue'])

        jobID = res['data']['jobs'][0]['id']
        print(jobID)

        # 查看作业详情
        detail_url = 'https://192.168.111.191/api/v1/job/detail?job_id={}&__timestamp__={}'.format(jobID,timestamp)
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        res = self.req.visit('get', detail_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        workdir = res['data']['work_dir']
        print(workdir)

        # 作业文件存储
        storage_url = 'https://192.168.111.191/api/v1/storage/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "path": workdir,
            "cross": False,
            "is_cloud": False,
            "user_name": "yskj",
            "filter_regexp_list": [],
            "show_hide_file": False
        }
        res = self.req.visit('post', storage_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Testbluntbody.sim", res['data'][0]['name'])
        self.assertEqual(4169521, res['data'][0]['size'])


    @allure.title("本地作业批量提交")
    def test_02BatchLocalJobSubmit_Success(self):
        """
        设置主文件--从我的文件/test-submit(请勿删除！！！)链接文件
        参数配置
        本地作业批量提交
        """

        with allure.step("步骤一:选择应用"):
            pass
        with allure.step("步骤二:从我的文件链接多个主文件"):
            pass
        with allure.step("步骤三:设置多个主文件"):
            pass
        with allure.step("步骤四：参数配置"):
            pass
        with allure.step("步骤五：点击提交按钮，确认提交"):
            print("作业提交成功，界面跳转到作业管理界面")

        createtempdir_url = 'https://192.168.111.191/api/v1/job/createTempDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "compute_type": "local"
        }
        res = self.req.visit('post', createtempdir_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        path = res['data']['path']
        print(path)

        link_url = 'https://192.168.111.191/api/v1/storage/link'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "cross": True,
	        "is_cloud": False,
	        "src_dir_paths": [],
	        "src_file_paths": ["yskj/test-submit(请勿删除！！！)/Blade.sim", "yskj/test-submit(请勿删除！！！)/STARCCM_test_Blade.sim", "yskj/test-submit(请勿删除！！！)/bluntbody.sim"],
	        "dst_path": path,
	        "current_path": "yskj/test-submit(请勿删除！！！)",
	        "user_name": "yskj"
        }
        res = self.req.visit('post', link_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])


        listofrecur_url = 'https://192.168.111.191/api/v1/storage/listOfRecur'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password),
            "Accept-Encoding": "gzip,deflate,br"
        }
        body = {
	        "paths": [path],
	        "cross": True,
	        "is_cloud": False,
	        "user_name": "yskj"
        }
        res = self.req.visit('post', listofrecur_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Blade.sim",res['data'][0]['name'])
        self.assertEqual("STARCCM_test_Blade.sim",res['data'][1]['name'])
        self.assertEqual("bluntbody.sim",res['data'][2]['name'])


        submit_url = 'https://192.168.111.191/api/v1/job/submit'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "app_id":"4ZR3n7tUN8A",
            "main_files": ["bluntbody.sim", "STARCCM_test_Blade.sim", "Blade.sim"],
            "queue_name":"",
            "work_dir":{"path":path,"is_temp":True},
            "fields":[{"id":"JOB_NAME","value":"BatchLocal","values":[],"type":"text"},
                      {"id":"CPU_NUM","value":"2","values":[],"type":"text"}]
        }
        res = self.req.visit('post', submit_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        #查询生成的作业情况
        """
        应用：jn2-STAR-CCM+ 10.02-R8.liuqi
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "job_types": [],
		        "start_time": None,
		        "end_time": None,
		        "job_id": "",
		        "job_name": "",
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4ZR3n7tUN8A", res['data']['jobs'][0]['app_id'])
        self.assertEqual("BatchLocal_Blade", res['data']['jobs'][0]['name'])
        self.assertEqual("BatchLocal_STARCCM_test_Blade", res['data']['jobs'][1]['name'])
        self.assertEqual("BatchLocal_bluntbody", res['data']['jobs'][2]['name'])
        self.assertEqual("local", res['data']['jobs'][0]['type'])
        self.assertEqual("2", res['data']['jobs'][0]['cpus_alloc'])
        self.assertEqual("workq", res['data']['jobs'][0]['queue'])


    @allure.title("云端作业单个提交")
    def test_03CloudJobSubmit_Success(self):
        """
        设置主文件--从我的文件/test-submit(请勿删除！！！)链接文件
        参数配置
        云端作业单个提交
        """

        with allure.step("步骤一:选择应用"):
            pass
        with allure.step("步骤二:从我的文件链接主文件"):
            pass
        with allure.step("步骤三:设置主文件"):
            pass
        with allure.step("步骤四：参数配置"):
            pass
        with allure.step("步骤五：点击提交按钮，确认提交"):
            print("作业提交成功，界面跳转到作业管理界面")

        #创建临时工作目录
        createtempdir_url = 'https://192.168.111.191/api/v1/job/createTempDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "compute_type": "cloud"
        }
        res = self.req.visit('post', createtempdir_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        path = res['data']['path']
        print(path)

        #hpc调用需要上传的文件
        hpcupload_url = 'https://192.168.111.191/api/v1/storage/hpcUpload/submitTask'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "overwrite": True,
	        "current_path": "./test-submit(请勿删除！！！)",
	        "dest_dir_path": path,
	        "src_dir_paths": [],
	        "src_file_paths": ["./test-submit(请勿删除！！！)/bluntbody.sim"],
	        "user_name": "yskj"
        }
        res = self.req.visit('post', hpcupload_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        hpc_upload_task = res['data']
        print(hpc_upload_task)

        #文件传输任务列表
        filetask_url = 'https://192.168.111.191/api/v1/storage/hpcUpload/fileTaskList?taskKey=hpc_upload_task&__timestamp__=1700191574767'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password),
            "Accept-Encoding": "gzip,deflate,br"
        }
        res = self.req.visit('get', filetask_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        time.sleep(3)
        #检查文件是否上传成功
        listofrecur_url = 'https://192.168.111.191/api/v1/storage/listOfRecur'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "paths": [path+"/"],
	        "cross": True,
	        "is_cloud": True,
	        "user_name": "yskj"
        }
        res = self.req.visit('post', listofrecur_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("bluntbody.sim",res['data'][0]['name'])

        #作业提交接口
        submit_url = 'https://192.168.111.191/api/v1/job/submit'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "app_id":"4YuMdnWkcSP",
            "main_files": ["bluntbody.sim"],
            "queue_name":"",
            "work_dir":{"path":path,"is_temp":True},
            "fields":[{"id":"JOB_NAME","value":"TestCloud","values":[],"type":"text"},
                      {"id":"CPU_NUM","value":"2","values":[],"type":"text"}]
        }
        res = self.req.visit('post', submit_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        #查询生成的作业情况
        """
        应用：jn-STAR-CCM+ 14.02
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "job_types": [],
		        "start_time": None,
		        "end_time": None,
		        "job_id": "",
		        "job_name": "",
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4YuMdnWkcSP", res['data']['jobs'][0]['app_id'])
        self.assertEqual("TestCloud", res['data']['jobs'][0]['name'])
        self.assertEqual("cloud", res['data']['jobs'][0]['type'])
        self.assertEqual("2", res['data']['jobs'][0]['cpus_alloc'])
        self.assertEqual("cloud", res['data']['jobs'][0]['queue'])


    @allure.title("云端作业批量提交")
    def test_04BatchCloudJobSubmit_Success(self):
        """
        设置主文件--从我的文件/test-submit(请勿删除！！！)链接文件
        参数配置
        云端作业单个提交
        """

        with allure.step("步骤一:选择应用"):
            pass
        with allure.step("步骤二:从我的文件链接多个主文件"):
            pass
        with allure.step("步骤三:设置多个主文件"):
            pass
        with allure.step("步骤四：参数配置"):
            pass
        with allure.step("步骤五：点击提交按钮，确认提交"):
            print("作业提交成功，界面跳转到作业管理界面")

        createtempdir_url = 'https://192.168.111.191/api/v1/job/createTempDir'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
            "compute_type": "cloud"
        }
        res = self.req.visit('post', createtempdir_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        path = res['data']['path']
        print(path)

        hpcupload_url = 'https://192.168.111.191/api/v1/storage/hpcUpload/submitTask'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "overwrite": True,
	        "current_path": "./test-submit(请勿删除！！！)",
	        "dest_dir_path": path,
	        "src_dir_paths": [],
	        "src_file_paths": ["./test-submit(请勿删除！！！)/Blade.sim", "./test-submit(请勿删除！！！)/bluntbody.sim"],
	        "user_name": "yskj"
        }
        res = self.req.visit('post', hpcupload_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        hpc_upload_task = res['data']
        print(hpc_upload_task)

        filetask_url = 'https://192.168.111.191/api/v1/storage/hpcUpload/fileTaskList?taskKey=hpc_upload_task&__timestamp__=1700191574767'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password),
            "Accept-Encoding": "gzip,deflate,br"
        }
        res = self.req.visit('get', filetask_url, headers=headers)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        time.sleep(5)
        listofrecur_url = 'https://192.168.111.191/api/v1/storage/listOfRecur'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "paths": [path+"/"],
	        "cross": True,
	        "is_cloud": True,
	        "user_name": "yskj"
        }
        res = self.req.visit('post', listofrecur_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("Blade.sim",res['data'][0]['name'])
        self.assertEqual("bluntbody.sim",res['data'][1]['name'])


        submit_url = 'https://192.168.111.191/api/v1/job/submit'
        headers = {
            "Cookie": PSPApi.GetCookie(url,name,password)
        }
        body = {
            "app_id":"4YuMdnWkcSP",
            "main_files": ["bluntbody.sim","Blade.sim"],
            "queue_name":"",
            "work_dir":{"path":path,"is_temp":True},
            "fields":[{"id":"JOB_NAME","value":"TestBatchCloud","values":[],"type":"text"},
                      {"id":"CPU_NUM","value":"2","values":[],"type":"text"}]
        }
        res = self.req.visit('post', submit_url, headers=headers,json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])

        #查询生成的作业情况
        """
        应用：jn-STAR-CCM+ 14.02
        """
        job_url = 'https://192.168.111.191/api/v1/job/list'
        headers = {
            "Cookie": PSPApi.GetCookie(url, name, password)
        }
        body = {
	        "page": {
		        "index": 1,
		        "size": 10
	        },
	        "filter": {
		        "app_names": [],
		        "states": [],
		        "queues": [],
		        "job_types": [],
		        "start_time": None,
		        "end_time": None,
		        "job_id": "",
		        "job_name": "",
		        "user_names": []
	        }
        }
        res = self.req.visit('post', job_url, headers=headers, json=body)
        print(res)
        # 根据请求结果中的code进行断言
        self.assertEqual(0, res['code'])
        self.assertEqual("4YuMdnWkcSP", res['data']['jobs'][0]['app_id'])
        self.assertEqual("TestBatchCloud_Blade", res['data']['jobs'][0]['name'])
        self.assertEqual("TestBatchCloud_bluntbody", res['data']['jobs'][1]['name'])
        self.assertEqual("cloud", res['data']['jobs'][0]['type'])
        self.assertEqual("2", res['data']['jobs'][0]['cpus_alloc'])
        self.assertEqual("cloud", res['data']['jobs'][0]['queue'])


if __name__ == '__main__':
    pytest.main(['-vs', 'test_job.py', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")