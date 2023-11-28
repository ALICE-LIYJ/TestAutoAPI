import os
from common import readFile

readfile = readFile

def env_para(env):
    """测试环境or线上环境"""
    if env == 'test':
        file_Path = os.path.dirname(os.path.dirname(__file__))
        yaml_Path = file_Path + '/config/test.yaml'
    else:
        file_Path = os.path.dirname(os.path.dirname(__file__))
        yaml_Path = file_Path + '/config/prod.yaml'
    return yaml_Path