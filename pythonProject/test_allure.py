import allure
import pytest
import os
import sys


@allure.feature('test_success')
def test_success():
    """this test succeeds"""
    assert True


@allure.feature('test_xfail_expected_failure')
@pytest.mark.xfail(reason='该功能尚未实现')
def test_xfail_expected_failure():
    print("该功能尚未实现")
    assert False


@allure.feature('test_xfail_unexpected_pass')
@pytest.mark.xfail(reason='该Bug尚未修复')
def test_xfail_unexpected_pass():
    print("该Bug尚未修复")
    assert True


'''当条件为True则跳过执行'''
@allure.feature("test_skipif")
@pytest.mark.skipif("darwin" in sys.platform,reason="如果操作系统是Mac则跳过执行")
def test_skipif():
    print("操作系统是Mac，test_skipif()函数跳过执行")


@allure.step("步骤一")
def test_with_nested_steps():
    passing_step()
    step_with_nested_steps()

@allure.step("步骤二")
def passing_step():
    pass


@allure.step("步骤三")
def step_with_nested_steps():
    nested_step()


@allure.step("步骤四")
def nested_step():
    nested_step_with_arguments(1, 'abc')


@allure.step("步骤五")
def nested_step_with_arguments(arg1, arg2):
    pass


@allure.title("动态标题: {param1} + {param2} = {expected}")
@pytest.mark.parametrize('param1,param2,expected', [(2, 2, 4),(1, 2, 3)])
def test_with_parameterized_title(param1, param2, expected):
    assert param1 + param2 == expected


if __name__ =='__main__':
    pytest.main(['-vs', 'test_allure.py','--clean-alluredir','--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")