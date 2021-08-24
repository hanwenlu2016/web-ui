# web-ui-auto 自动化框架


 [！！！！推荐一个便宜还不错的梯子VPN](https://eatpeach.top/auth/register?code=3p0I)


```css 
 * 各位有兴小伙伴麻烦点下start 谢谢 😁
``` 


###### 设计思路

  web-ui-auto分为 C端 (python+selenium+pytest+allure) 实现测试用例代码输入输出执行，M端(django+rest_framework+react*M端暂未开源功能还未开发完成) 
做用例管理，定时任务分配，测试工具集合。


> ~~！！！ M端(django+rest_framework+react）此部分由于设计到公司的业务暂时不做了开源！！！~~


```css 
-- 不过本人目前找时间在重新写一个M端管理平台 (django+mtv模式)
```

初步效果如下 [对应项目](https://github.com/hanwenlu2016/Salvation) 有时间持续更新！：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/001.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/003.png)


###### 使用说明
 
1 本架构元素定位 数据依赖为yaml文件 

2 使用前需要对 读取yaml函数(yaml_data.py) ，yaml对应说明仔细阅读 文件内代码处有注释！

3 web-base.py 为 web函数封装 已经封装了功能代码 可以仔细阅读注释来完成页面功能！

4 app_base.py 为 app函数封装 可以仔细阅读注释来完成页面功能

5 api_base.py 为 api接口函数封装 可以仔细阅读注释来完成页面功能

6 目前 web 端用例管理和任务定时触发已经在调试阶段，如果顺利可开源让大家参考！

7 目前浏览器支持 ctenos7(谷歌/火狐)， windos(谷歌/火狐/IE)，mac(谷歌/火狐/safair) 其它浏览器暂未联调！


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


> ~~！！！ 管理技术由 django+rest_framework+react实际 主要来管理C端用列，定时任务自动跑任务，工具集成等！ 此部分由于设计到公司的业务暂时不做了开源！！！~~




管理端用户页面--此部分应用用 [Salvation](https://github.com/hanwenlu2016/Salvation)  替代

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/manage0.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/manage1.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/manage2.png)



管理端管理员后台：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin1.png)



![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin2.png)


# 更新日志

2021 -07 -29

优化沉余代码，调整部分类结构修复BUG。

2021 -08 -23

增加多步骤兼容输入问题。

