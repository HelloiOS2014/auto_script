# 胖虎的自动化脚本使用教程

## 使用前必读

### 系统要求

> 操作系统
>>Windows
>>macOS
>>Linux

>Python环境
>>Python2.7 & Python3.3+

### 脚本使用的前置条件

> 安装adb
> 安装Python
> 安装airtest

#### 安装adb

adb的安装非常简单，总共两种途径，一种是下载abd的压缩包解压即可([教程如下](https://gitee.com/ly.cn/auto_script/blob/master/adb/adb%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B.md))，另一种是直接安装Android Studio。

#### 安装Python

参考这个[菜鸟教程](https://www.runoob.com/python/python-install.html)

#### 安装airtest

目前AirtestIDE提供了Windows、Mac和Linux的客户端，直接点击[Airtest官网](https://airtest.netease.com/)即可安装下载

## 开始使用

### 设备连接

> 掏出手机
> 插上数据线连接电脑（Mac或Windows）
> 启动AirtestIDE
> adb连接

如下图
![连接示意图](https://s2.loli.net/2022/01/12/BplS5FetTPhikmg.jpg)

### 导入脚本

导入相对应脚本，选择 *.air或*.py 即可。
如下图
![导入脚本](https://s2.loli.net/2022/01/12/BplS5FetTPhikmg.jpg)

### 修改参数

修改<font color= #00FFFF>min_support</font>(数据采集条件)，<font color= #00FFFF>export_path</font>(数据存储地址)、<font color= #00FFFF>search_text</font>(搜索关键词)
如下图
![修改参数](https://s2.loli.net/2022/01/12/z4xespiFmXHVLkM.jpg)

### 运行脚本

点击运行即可
![运行脚本](https://s2.loli.net/2022/01/12/F5y9h3KXqwQPkJj.jpg)
