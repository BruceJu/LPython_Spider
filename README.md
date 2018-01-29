# LPython_Spider

## 概述

> LPython项目目前设置了3个模块，分别是基于Python的 `文章`  ,`视频`  `招聘信息`数据来自知名博客，招聘信息信息站，在结构上使用scrapy,redis, mongodb,graphite实现的一个分布式网络爬虫,
底层存储mongodb集群,分布式使用redis实现,爬虫状态显示使用graphite实现。

- [x] 支持分布式
- [x] 支持Redis动态配置和脚本处理
- [x] 支持防ban
- [x] 支持动态抓取
- [x] 支持自动关闭
- [x] 支持过程可视化监控
- [x] 支持可视化部署，及管理
- [x] 支持异常状态收集，与重试
- [x] 支持运行状态的邮件通知

## TodoList





### 文章模块
> 对于文章模块，目前将针对 '伯乐在线'，'简书'，'头条'，'CSDN',的中的有关Python的信息进行抓取，会采用分布式爬虫，定向爬虫进行抓取，在存储上，采用MongDB分布式存储，另外由于LPython项目还存在移动端的部分，小程序中要求使用Https传输协议，为了节省成本，在存储数据时，还会用使用 LeanCloud后端云进行数据的备份存储，方便移动端的调用。


* 数据来源
  * 伯乐在线
  * 简书
  * 头条

* 数据获取
  * 分布式爬虫
  * 定向爬虫
  * 分析网络请求所获取的RestFulAPI
  
* 数据存储
  * MongoDB 分布式存储
  * LeanCloud 后端云存储
  
### 伯乐在线

> 伯乐在线 的URL设计对于 爬虫来说十分友好，也不存在需要Spider动态技术抓取的页面，方便爬取，在爬取上，将采用分布式的结构直接进行爬取。

* 目标链接 ：http://python.jobbole.com/all-posts/
* 抓取方式 ：分布式
* 抓取内容 
   * 标题
   * 发布时间
   * 简介
   * 分类
   * 文章URL
   * 封面URL
   
### 关于数据存储
> 在存储上我们采用了俩种存储方式，一种是分布式存储，另一种是后端云存储，之所以会有俩种存储方式是因为，小程序和Android端需要有RESTfulApi，
而且小程序还需要验证证书，而且我们目前还没有真正服务器的资源，所以现阶段只能使用后端云的方式来存储数据，之后准备用Django或者Flask来搭一个
WEB服务，来解决这些问题

> 之后我们在进行分布式时，会先将数据同步至redis的中，方便以后的集中处理，提供给MongoDB和 ES使用，来构建搜索引擎
> 分布式使用的是 Redis,和Scrapy-redis的实现的，Redis用来缓存各个爬虫生成的Request，和存储过滤请求的指纹信息

#### 关于分布式搭建以及运行中，遇到的问题

##### 问题.多台客户端连接 'redis' 但是只有一个能够响应到`redis`
> 有俩台机器，Windows电脑A，和Ubuntu电脑B，redis server部署在 Windows电脑A上，在电脑A,B启动爬虫后，俩只爬虫都进入监听状态，在redis中进行 url的lpush操作，
奇怪的事情发生了，电脑A，或者电脑B中只有一台电脑能监听到 redis,但是具体哪个能够监听到这个很随机，有时是电脑A，有时是电脑B,也就是说只有一个爬虫能够正常请求
被这个问题困扰了3天，最后，又完完全全的刨析了一次，源码才解决这个，关于这个问题的详细描述和运行状态截图，以及排重思路，解决办法可以查看这里
[scrapy-redis多台机器部署，但只有一台可执行的问题](https://segmentfault.com/q/1010000012925625)

##### 问题.没有服务器资源，使用个人电脑，会面临IP更换频繁的问题，会造成需要手动修改好几处IP
> * 针对这个问题，是采用了一种配置文件的方式，来解决的，建立一个json文件，将使用的值配置进去
> * 编写了一个`config.py`的类，使用属性方法的模式来读取配置文件的信息和建立关系信息
> * 具体可以参考，项目结构中的`config.py`这个文件。
> * 使用上可以参考，Setting.py中的 `REDIS_HOST` 和 `REDIS_PORT`的配置方式
> * 部分代码
  
  ```python
    @property
    def redis_host(self):
        return self._redis_host

    @redis_host.setter
    def change_default_redis_host(self,value):
        self._redis_host = value

    @property
    def redis_port(self):
        return self._redis_port

    @redis_port.setter
    def change_defaule_redis_port(self,value):
        self._redis_port = value
`````
##### 问题.在调试和启动分布式Spider的过程中，需要频繁的在 redis-cli中执行lpush操作，很麻烦
> * 针对这个问题，是编写了一个 `RedisHelper.py` 使用单例模式来连接客户端，
> * 并封装了 启动，增，删，改，查，的方法，来操作`redis`
> * 具体可参考 `RedisHelper.py`这个文件，部分代码如下
```python
class RedisManager(Singleton):
    def __init__(self):
        self.config = spiderConfig
        self.redis_server = redis.Redis(host=self.config.redis_host, port=self.config.redis_port)
        if self.redis_server.ping():
            log.logger.info('connect redis-server successful!!!')
        else:
            log.logger.info('connect redis-server fail!!!')

            raise Exception

    def doInitPush(self):
        try:
            self.redis_server.lpush(self.config.jobbole_redis_key, self.config.jobbole_push_url)
            print "写入url成功!"
            thread = threading.Thread(target=self.doQuery, args=(), name='thread-redis')
            thread.start()
            thread.join(120)
            print "completed Bye "
        except Exception:
            print "写入失败"
```  
##### 问题.配置文件操作类的路径引用方式和字符串编码不同导致的，在不同平台上无法运行的bug
>* 在操作 `config.json`时，由于使用的路径中使用了`\`,导致了在Linux上会报错.
>* 例如`\LPythonSpider\config.json`这样的写法在Windows上可以运行，但是在Linux上就会报错
>* 针对这个问题，要使用os模块来引用路径，代码如下
```python
   BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
   LPYTHONSPIDER = os.path.join(BASE_DIR, 'LPythonSpider')
   CONFIG_FILE = os.path.join(LPYTHONSPIDER, 'config.json')
   self.config = codecs.open(CONFIG_FILE, 'rb', 'utf-8')
```

##### 问题.爬取过程中，由于代理IP的无效导致的404爬取页面的收集
> * 针对这个问题是按照这样的机制来操作的
> * 首先针对无效的Response的进行重试。
> * 当重试无效后，进行记录。
> * 参考了scrapy的`Retry.py`这个中间件
> * 在此基础上增加了，重试后仍然失败的页面的收集功能。
> * 具体可参考`InvalidResponseRetryRecordMiddleware` 这个中间件
> * 最后收集的结果是在`InvalidResponseMessage.json`(名字可通过ConfigHelper.py更改)下面这个样子的
```json
{"url": "http://www.dmoz.org/", "retries": 3, "reason": "403 Forbidden"}

```
> * 部分代码如下
```python
    def _retry(self, request, reason, spider,response):
        retries = request.meta.get('retry_times', 0) + 1
            .................此处省略........................
        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries   
             .................此处省略........................
            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            .................此处省略........................
            reason = response_status_message(response.status)
            dict_response = {'url': request.url, 'reason': reason, 'retries': retries}
            lines = json.dumps(dict_response, ensure_ascii=False) + "\n"
            self.record_file.write(lines)
            return response
```




#####  问题.分布式架构爬取完成后，如何关闭爬虫
>* 针对这个问题，我目前采用的是使用Scrapy的 `EXTENSIONS` 中的`CloseSpider`
>* 当爬虫处于空闲状态时，超过了设定的时间范围，自动关闭。
>* 目前设置的值是120秒，部分代码如下
```python
EXTENSIONS = {
    'scrapy.exceptions.CloseSpider':500
}
CLOSESPIDER_TIMEOUT = 120
```
    
##### 问题.爬虫发生错误时如何及时响应，并以邮件的形式通知,这里补充发送邮件的逻辑
>* 写了一个中间件，响应信号，在爬虫关闭`spider_close`时，和发生错误时`spider_error`，进行邮件通知，
>* 这里没有使用`scrapy`的内置邮件模块，因为在使用内置模块时，总出现问题
>* 所以这里自己实现了发送邮件的逻辑。具体参考`StatsAndErrorMailer`这个类部分代码如下
```python
    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        body = "Global stats\n\n"
        body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        body += "\n\n%s stats\n\n" % spider.name
        body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        return sendmail(body,self.recipients,"Scrapy stats for: %s" % spider.name)

    def spider_error(self,failure, response, spider):
        body = "Meet Error\n\n"
        body += "\n\n%s error\n\n" % spider.name+"\n"
        body += " ".join("error message is  : %s" % failure.getErrorMessage)
        body += " ".join("error response url is  : %s" % response.url)
        return sendmail( body,self.recipients, "Scrapy meet a error for: %s" % spider.name)

```
#### 问题.如何避免每次启动重复爬取

#### 问题.如何将分布式爬虫服务化

#### 问题.如何以web服务的方式监控爬虫运行
  
 
