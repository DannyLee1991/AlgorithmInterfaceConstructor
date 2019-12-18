# 算法接口构造器

AIC

## 使用方式

安装:

```
pip3 install aic
```

在算法所在的根目录下编写配置文件`manifest.yaml`,配置文件示例如下：

```
# - 入口包名/方法/参数
app:
  # 应用名称
  name: demo
  # 版本
  version: 1.0
  rpc:
    # 对外暴露的方法所在的包名 以及方法名 和注释
    - pkg: demo.algorithm.model
      func: func
      note: 测试方法
  docker:
    # 端口
    port: 6565
    # dockerfile中需要注入的命令
    cmd:
      - COPY --from=builder /data/resnet50-19c8e357.pth /root/.torch/models/
      - ADD sources.list /etc/apt/sources.list
      - RUN apt update && apt -y install python3-opencv
```

编写完之后，在当前目录下执行:

```
aic
```

即可自动生成rpc接口。