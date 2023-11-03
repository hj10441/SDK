# testcase-eda-sdk
主要用于生产环境冒烟执行,生产环境jupyter提供Python3.6和python3.9 两个环境，sdk只能用于这两个版本的python。

## online bugs 
这个文件夹里放的是线上bug对应的用例，文件名以test_{issue号}命名，例如test_22314.py

## requirements
requirements36.txt 放的是jupyter3.6 依赖的包
requirements39.txt 放的是jupyter3.9 环境依赖的包
本身测试用例需要的包，请放到requirements.txt文件里。