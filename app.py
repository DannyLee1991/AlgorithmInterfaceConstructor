import ast
import yaml
import click
import os
import shutil

_START_SCRIPT = "server.py"
_MANIFEST_YAML = "manifest.yaml"
_DOCKER_FILE = "Dockerfile"
_DEFAULT_DOCKER_FILE_TPL = """FROM registry.cn-beijing.aliyuncs.com/tlab/busybox:torch as builder

FROM python:3.7

{cmd}

WORKDIR /app

ADD requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE {port}

ENV TZ="Asia/Shanghai" PARAMS=" "

CMD python server.py $PARAMS
"""

_START_SCRIPT_CODE = """from grpclib import *

if __name__ == '__main__':
    server = GrpcServer()
    server.run()
"""


@click.group()
def cli():
    pass


def find_manifest():
    if os.path.exists(_MANIFEST_YAML):
        with open(_MANIFEST_YAML, 'r') as f:
            return yaml.safe_load(f)


def parse_manifest(manifest):
    """
    解析清单文件
    :param manifest:
    :return:
    """
    if manifest:
        app = manifest['app']
        rpc_items = []
        if 'docker' in app and 'tpl' in app['docker'] and app['docker']['tpl'] and os.path.exists(app['docker']['tpl']):
            with open(app['docker']['tpl'], 'r') as f:
                app['docker']['tpl'] = f.read()
        else:
            app['docker']['tpl'] = _DEFAULT_DOCKER_FILE_TPL
        for item in app['rpc']:
            pkg = item['pkg']
            func_name = item['func']
            note = item['note']

            with open(os.sep.join(str(pkg).split('.')) + ".py", 'r') as f:
                ast_tree = ast.parse(f.read())
                for func in ast_tree.body:
                    if func.name == func_name:
                        arg_names = [arg.arg for arg in func.args.args]
                        rpc_items.append((pkg, func.name, arg_names, note))
        return app, rpc_items


def _remove_if_exist(path):
    if os.path.exists(path):
        os.remove(path)


def clear_env():
    shutil.rmtree('rpc', ignore_errors=True)
    _remove_if_exist(_DOCKER_FILE)
    _remove_if_exist(_START_SCRIPT)


def create_rpc(app, rpc_items):
    os.makedirs('rpc', exist_ok=True)
    with open('rpc/__init__.py', 'w') as f:
        pass
    py_file_name = app['name'].capitalize() + "RpcServer.py"
    py_file_path = os.path.join('rpc', py_file_name)
    with open(py_file_path, 'w') as f:
        write_line_func = lambda level=0, code="": f.write(
            "{indent}{code}".format(indent=level * "\t", code=code))
        # 写入import逻辑
        for rpc_item in rpc_items:
            write_line_func(level=0,
                            code="from {pkg} import {func} as {_func}".format(pkg=str(rpc_item[0]),
                                                                              func=str(rpc_item[1]),
                                                                              _func="_" + str(rpc_item[1])))
        f.write(os.linesep * 3)

        for rpc_item in rpc_items:
            func_name = rpc_item[1]
            _func_name = "_" + func_name
            arg_names = rpc_item[2]
            note = rpc_item[3]
            # 方法名
            write_line_func(
                level=0,
                code="def {func_name}({args}):".format(func_name=func_name, args=", ".join(arg_names)) + os.linesep)
            # 注释
            if note:
                write_line_func(level=1, code="\"\"\"" + os.linesep)
                write_line_func(level=1, code=note + os.linesep)
                write_line_func(level=1, code="\"\"\"" + os.linesep)
            write_line_func(level=1,
                            code="return {func_name}({args})".format(func_name=_func_name, args=", ".join(arg_names)))


def create_docker(app):
    with open(_DOCKER_FILE, 'w') as f:
        tpl = app['docker']['tpl']
        app['docker'].pop('tpl')
        fmt_args = {}
        for k in dict(app['docker']).keys():
            v = app['docker'][k]
            if type(v) == list:
                fmt_args[k] = os.linesep.join(v)
            else:
                fmt_args[k] = v
        f.write(tpl.format(**fmt_args))


def create_startpy():
    """
    创建启动脚本
    :return: 
    """
    with open(_START_SCRIPT, 'w') as f:
        f.write(_START_SCRIPT_CODE)


@cli.command()
def aic():
    # 找到yaml
    manifest = find_manifest()
    # 解析yaml
    app, rpc_items = parse_manifest(manifest)
    assert (app and rpc_items), "manifest文件解析异常"
    # 清空构建目录
    clear_env()
    # 构建rpc接口
    create_rpc(app, rpc_items)
    # 构建Dockerfile
    create_docker(app)
    # 构建启动脚本
    create_startpy()


# click.echo("test")


# yaml.load()

if __name__ == '__main__':
    aic()
