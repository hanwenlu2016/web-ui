# ** 最近发现部分人员拿着我们开源的项目描述为自己所写 坚决抵制此行为 请遵守Apache License 2.0 开源协议

# web-ui-auto 自动化框架

```css 
 * 各位有兴小伙伴麻烦点下start 谢谢 😁
``` 

### 设计思路:

web-ui-auto分为 C端 (python+selenium+pytest+allure) 实现测试用例代码输入输出执行，M端
做用例管理，定时任务分配，测试工具集合。


初步效果如下 [对应项目](https://github.com/hanwenlu2016/Salvation) 有时间持续更新！：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/001.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/003.png)

### 后台管理端：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin1.png)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/admin2.png)

### 项目框架设计图：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/frame.png)

### 项目架构详情：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/frameexplains.png)

### 测试输出报告：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/run001.jpg)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/run002.jpg)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/run003.jpg)

### seleniumGrid集群：

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/run3.jpg)

![](https://github.com/hanwenlu2016/web-ui/blob/main/doct/img/run4.jpg)

# 开始使用

### 1开始准备

```python
# 安装所需的依赖环境(阿里源安装 * 操作系统中必须有python3, 推荐python3.8或者更高版本)

pip
install - r
requirements.txt
https: // mirrors.aliyun.com / pypi / simple

# 安装配置Allure(官网下载解压包)

解压allure - commandline - 2.13
.6.zip
包到对应目录

把
allure - commandline - 2.13
.6 / bin
加入到环境变量

打开控制台输入: allure - -version
出来版本代表安装成功

# 运行(run.py 文件即可)

python3
run.py

```

### 2使用说明

1 本架构元素定位 数据依赖为yaml文件

2 使用前需要对 yaml模板的熟悉 参考（databse/file/test_demo_yaml）注释说明

3 web-base.py 为 web函数封装 已经封装了功能代码 可以仔细阅读注释来完成页面功能！

4 app_base.py 为 app函数封装 可以仔细阅读注释来完成页面功能

5 目前 web 端用例管理和任务定时触发已经在调试阶段，如果顺利可开源让大家参考！

6 目前浏览器支持 ctenos7(谷歌/火狐)， windos(谷歌/火狐/IE)，mac(谷歌/火狐/safair) 其它浏览器暂未联调！

# 更新日志

2022 -10 -12

修复多步骤等待时间不生效问题

2022 -06 -10

增加yaml模板支持iso 和android 同时类型的特殊定位方式 对移动端web浏览器兼容跟友好

2022 -06 -07

主分支删除API接口功能，基于yaml做参数配置。优化导入已经代码。

2022 -02 -23

增加企业微信 钉钉群机器人通知文本功能，增加生产环境传递参数

2022 -02 -22

增加对邮箱结果发送支持 优化联动代码逻辑

2022 -01 -07

增加对ddddocr支持 读取图片验证码功能`


