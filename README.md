# web-ui-auto 自动化框架

###### 设计思路

web-ui-auto分为 C端 (python+selenium+pytest+allure) 实现测试用例代码输入输出执行，M端(django+rest_framework+vue *M端暂未开源功能还未开发完成) 做用例管理，定时任务分配，测试工具集合。

###### 项目框架设计图

![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\frame.png)

###### 项目架构详情

![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\frameexplain.png)

###### 测试输出报告

![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\testresult.png)

###### 开始准备使用

操作系统中必须有python3, 推荐python3.8或者更高版本



```python
# 安装所需的依赖环境(阿里源安装)

pip install -r requirements.txt https://mirrors.aliyun.com/pypi/simple  
    
# 安装配置Allure(官网下载解压包)

解压allure-commandline-2.13.6.zip 包到对应目录

把 allure-commandline-2.13.6/bin 加入到环境变量

打开控制台输入:  allure --version   出来版本代表安装成功
    
# 运行(main 目录运行 run.py 文件即可)

python3 run.py

  
```

###### 支持的浏览器

- [ ] - [ ] - [ ] | **Chromium** | 支持     |
      | :----------: | -------- |
      | **Firefox**  | **支持** |
      |    **Ie**    | **支持** |

###### 后期更新

管理端功能暂未开发完成，请关注项目。完成后会选择上传开源！



管理技术由 django+rest_framework+react实际 主要来管理C端用列，定时任务自动跑任务，工具集成等！



管理端用户页面



![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\manage1.png)

![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\manage2.png)



管理端管理员后台：

![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\admin1.png)



![](D:\My-Svn-oprject\github\web-ui-auto\doct\img\admin2.png)# web-ui
