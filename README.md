# 实验二：《Python应用开发》登录爬取与数据存储 (10学时) :smile:
## 目录
- [一、实验描述](#实验描述)
- [二、基本要求](#基本要求)
- [三、工具/准备工作](#工具准备工作)
- [四、评分规则](#评分规则)
- [五、运行注意事项](#运行注意事项)

### 一、实验描述
实验名称:登录爬取与数据存储

#### 实验目的
-1. 理解和熟悉网页登录式爬虫；
-2. 能够通过模拟登录请求或者移植Cookie来实现登陆式爬取；
-3. 能够使用常见的数据库对数据进行存储。

#### 实验环境
Python3

Pip3

#### 实验内容:论坛数据爬取系统
- 1.daluom.com是专门讨论温州地区城市发展主题的本地论坛，需要登陆账号来访问帖子数据。
- 2.bbs.nga.cn是一个较大的互联网游戏论坛，同样需要登陆账号来访问帖子数据。该论坛具有帖子回收机制，一些老旧的帖子会被删除。

请在上述两个论坛中选择一个论坛，并对论坛中最活跃的版块进行数据爬取和数据存储。具体任务包括：
- 1.爬取该论坛50页历史数据，获取数据包括每个帖子的链接、发布时间、标题、楼主ID、帖子内容、跟帖ID、跟帖时间、跟帖内容（仅限文字部分，图片可不进行处理）。
- 2.针对上述爬取数据，将数据同时存储到MySQL数据库或者内存数据库Redis。

#### 实验报告关键内容
- 1.描述网站爬取的思路包括起始页面、爬取的路径、设计思路等；
- 2.展示一个帖子的数据爬取结果，对比原始网页数据；
- 3.描述数据库的存储方式的设计；
- 4.展示数据库数据结果，可截图。
可选加分实验，有一定难度
- 1.通过模拟登录请求，验证码自动化处理或者手动输入。
- 2.Fiddler Classic获取NGA论坛APP的流量，提取API，通过API进行爬取。

### 二、基本要求:
- 1.实现相关系统功能；
- 2.实现系统部署和运行；
- 3.提交一份实验报告，写什么。

### 三、工具/准备工作    
- 1.复习上学期Python应用开发理论及实验相关内容
- 2.熟悉Python编程语言，IDE的使用

### 四、评分规则
- 1.根据系统上的提交情况以及实验报告打分。
- 2.分值分配：系统功能实现占50%，实验报告书面情况及内容占50%。
- 3.严禁抄袭！发现后所有雷同均0分。

### 五、运行注意事项
- 先运行get_cookie.py获取cookie，再运行main.py运行爬虫。:adult: