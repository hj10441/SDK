# testcase-eda-sdk
主要用于生产环境冒烟执行,生产环境jupyter提供Python3.6和python3.9 两个环境，sdk只能用于这两个版本的python。

## testcases
存放测试用例

### smokedemos
这个文件夹里放的是jupyter demo对应的测试用例

### online bugs 
这个文件夹里放的是线上bug对应的用例，文件名以test_{issue号}命名，例如test_22314.py

### testapis
放的是对sdk api的校验，包括eda用户手册里提供的demo

## testdata
这个文件夹放的是测试数据

## requirements
requirements36.txt 放的是jupyter3.6 依赖的包
requirements39.txt 放的是jupyter3.9 环境依赖的包
本身测试用例需要的包，请放到requirements.txt文件里,注意：*不要指定版本，因为服务器上环境是3.6，和开发机的python版本大概率不同*

# 注释格式说明
每个测试用例下使用''' '''注释说明测试用例的检查点（如下），第一行是总结,会作为Gaia平台上显示的用例名字
```
  '''查询数据资产的数据模型
    检查点：
        1. 列表是否2列，列名是否正确
        2. 返回的数据个数大于0
  '''

```