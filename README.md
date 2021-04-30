# web-ui-auto 自动化框架

###### 设计思路

web-ui-auto分为 C端 (python+selenium+pytest+allure) 实现测试用例代码输入输出执行，M端(django+rest_framework+vue *M端暂未开源功能还未开发完成) 做用例管理，定时任务分配，测试工具集合。

###### 使用说明

1 本架构元素定位 数据依赖为yaml文件

2 使用前需要对 读取yaml函数已经(yaml_data.py) ，yaml对应说明仔细阅读 文件内代码处有注释！

3 web-base.py 为 web函数封装 已经封装了功能代码 可以仔细阅读注释来完成页面功能！

4 app_base.py 为 app 函数封装 可以仔细阅读注释来完成页面功能

5 目前 web 端用例管理和任务定时触发已经在调试阶段，如果顺利可开源让大家参考！

6 目前浏览器支持 ctenos7(谷歌/火狐)， windos(谷歌/火狐/IE)，mac(谷歌/火狐/safair) 其它浏览器暂未联调！


###### 项目框架设计图

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/frame.png)

###### 项目架构详情

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/frameexplain.png)

###### 测试输出报告

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/testresult.png)

###### 开始准备使用

操作系统中必须有python3, 推荐python3.8或者更高版本



```python
# 安装所需的依赖环境(阿里源安装)

pip install -r requirements.txt https://mirrors.aliyun.com/pypi/simple  

    
# 安装配置Allure(官网下载解压包)

解压allure-commandline-2.13.6.zip 包到对应目录

把 allure-commandline-2.13.6/bin 加入到环境变量

打开控制台输入:  allure --version   出来版本代表安装成功
    
# 运行(run.py 文件即可)

python3 run.py

  
```



###### 后期更新

管理端功能暂未开发完成，请关注项目。完成后会选择上传开源！



管理技术由 django+rest_framework+react实际 主要来管理C端用列，定时任务自动跑任务，工具集成等！



管理端用户页面



![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/manage1.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/manage2.png)



管理端管理员后台：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin1.png)



![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin2.png)


# 更新日志
2021 -02 -05

支持 iso 调整架构目录优化函数类！！！！！

2021 -03 -25

调整架构目录！优化多余代码，支持selenium分布式！


2021 -04 -02

yaml文件定位用例数据分离，代码优化！

