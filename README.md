# LPython_Spider

## 在线文档
> [详细文档地址](https://bruceju.github.io/LPython_Spider/#/)

## 概述
> LPython项目的采集端目前设置了3个模块，分别是基于Python的 `文章`  ,`视频`  `招聘信息`数据来自知名博客，招聘信息信息站，在结构上使用scrapy,redis, mongodb,graphite实现的一个分布式网络爬虫,
底层存储mongodb集群,分布式使用redis实现,爬虫状态显示使用graphite实现。

- [x] 支持分布式
- [x] 支持定时自动执行
- [x] 支持Redis动态配置和脚本处理
- [x] 支持防ban
- [x] 支持动态抓取
- [x] 支持自动关闭
- [x] 支持异常状态收集，与重试
- [x] 支持运行状态的邮件通知
- [x] 支持运行状态的微信通知
- [x] 支持命令行控制