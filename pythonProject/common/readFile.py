import os

import yaml

filePath = os.path.dirname(os.path.dirname(__file__))
yamlPath1 = filePath + '/config/test.yaml'


def read_yaml(yaml_Path):
    """
    读yaml文件
    :return:
    """
    try:
        with open(yaml_Path, 'r', encoding='utf-8') as f:
            x = yaml.load(f.read(), Loader=yaml.FullLoader)
        return x
    except Exception as e:
        print("读yaml文件报错{}".format(e))


def write_yaml(key, new_data):
    old_data = read_yaml(yamlPath1)
    old_data[key] = new_data
    try:
        with open(yamlPath1, 'w', encoding='utf-8') as f:
            yaml.dump(old_data, f)
    except Exception as e:
        print("写yaml文件报错{}".format(e))


if __name__ == '__main__':
    # filePath = os.path.dirname(os.path.dirname(__file__))
    pass
