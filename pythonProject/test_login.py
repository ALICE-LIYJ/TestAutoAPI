import unittest
import allure
import os
import pytest
from common.requests_handler import RequestHandler

@allure.epic("PSP")
@allure.feature("登录功能")
#写法一：@allure.severity(allure.severity_level.CRITICAL)
#写法二：@allure.severity("critical")
#blocker：阻塞缺陷（功能未实现，无法下一步）
#critical：严重缺陷（功能点缺失）
#normal： 一般缺陷（边界情况，格式错误），不填写时默认为normal
#minor：次要缺陷（界面错误与ui需求不符）
#trivial： 轻微缺陷（必须项无提示，或者提示不规范）

class TestLogin(unittest.TestCase):
    def setUp(self):
        #请求类实例化
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()


    @allure.severity("critical")
    @allure.title("正确的用户名、密码登录")
    def test_login_success(self):
        """
        正确的用户名、密码
        """
        with allure.step("step1:输入正确的用户名、密码"):
            print("输入正确的用户名、密码")
        with allure.step("step2:校验登录结果：登录成功"):
            print("登录成功")
        login_url = 'https://192.168.111.191/api/v1/auth/login'
        body = {
            "name":"yskj",
            "password":"yskj2407"
        }

        res = self.req.visit('post',login_url,json=body)
        #根据请求结果中的code进行断言
        print(res)
        self.assertEqual(0,res['code'])


    @allure.title("错误的用户名、正确的密码登录")
    def test_login_wrong_name(self):
        """
        错误的用户名、正确的密码
        """

        with allure.step("step1:输入错误的用户名、正确的密码"):
            print("输入错误的用户名、正确的密码")
        with allure.step("step2:校验登录结果：登录失败，报错提示：用户不存在"):
            print("登录失败")

        login_url = 'https://192.168.111.191/api/v1/auth/login'
        body = {
            "name": "yskj11",
            "password": "yskj2407"
        }

        res = self.req.visit('post', login_url, json=body)
        # 根据请求结果中的code进行断言
        self.assertEqual(16020, res['code'])
        #根据请求结果中的message进行断言
        self.assertEqual("用户不存在",res['message'])


    @allure.title("正确的用户名、错误的密码登录")
    def test_login_wrong_pwd(self):
        """
        正确的用户名、错误的密码
        """

        with allure.step("step1:输入正确的用户名、错误的密码"):
            print("输入正确的用户名、错误的密码")
        with allure.step("step2:校验登录结果：登录失败，报错提示：账号有误，登录失败"):
            print("登录失败")

        login_url = 'https://192.168.111.191/api/v1/auth/login'
        body = {
            "name": "yskj",
            "password": "yskj2411"
        }

        res = self.req.visit('post', login_url, json=body)
        # 根据请求结果中的code进行断言
        self.assertEqual(16002, res['code'])
        #根据请求结果中的message进行断言
        self.assertEqual("账号有误，登录失败",res['message'])


if __name__ == '__main__':
    pytest.main(['-vs', 'test_login.py', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")