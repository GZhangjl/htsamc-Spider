# htsamc-Spider

### 基本情况

* 通过`chrome`浏览器开发者工具分析网页，发现在未登录状态下可直接获取公告列表页中公告的名字和对应`PDF`文件下载链接，但是却无法获得当前具体的页数（页数信息不是静态加载的），所以如果直接将该页面设为爬虫入口，则最多只能爬取首页

* 继续通过浏览器开发者工具进行分析，发现当进行翻页操作时，本地会向服务器发送一个请求，该请求的URL非常具有特征性: *http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage=10* 尝试修改`rowOfPage`参数后请求会发现页面会跳转到显示相应数量公告的页面，于是只要在浏览器中看到共有几页，再通过计算得到总共的公告数量，就能通过设置`rowOfPage=总数`进行所有公告的获取和下载

* 在进行代码编写时，为了节约资源以及保证公告文件的时效性，于是考查网页上每个公告的创建时间，每次爬取时只下载离爬取日期两周以内的文件；在数据储存时不区分时效，而是将所有公告进行信息存储

	* 公告时效性下载的实现，主要是通过设定不同`pipeline`之间传递`item`的顺序实现,`DateProcessorPipeline`用于比较创建时间和爬取时间的时间差，如果符合要求（`item`属性`is_recent`值为`True`）则将`item`传递给`MyFilesPipeline`用于下载，如果`is_recent`值为`False`，那么该`pipeline`就返回空字典`{}`，这样下一个`pipeline`也无法处理

	* 这次爬虫最终的数据计划是存储在`CSV`文件中，存储过程使用了`scrapy.exporters`模块中的`CsvItemExporter`类,通过阅读文档了解了这个类的使用方法，最终存储成功

	* `MyFilesPipeline`继承了`Scrapy`默认的`FilesPipeline`类，通过重写`item_completed`与`item_completed`方法修改了下载后`PDF`的名字以及用于保存的文件夹的名字

* 以上基本达成最初爬虫目的

### 完成改进

* 最大的改进：为了进一步自动化爬取，意图通过程序获得网页中公告的总页数

* 关于爬取网页进行过两次改进
	
	* 第一次为通过`Selenium`进行模拟访问页面，直接从加载完毕的网页中获取公告总页数，然后计算总的公告数，通过修改`rowOfPage`参数进行爬取，除了总页数获取方式有了进步，其余思路与上述一致
	
	* 第二次是发现 *http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage=10* 这个`URL`在原来的请求中是`POST`请求，而非`GET`请求，这个请求带上的表单数据包括页数和每页显示的公告数，于是便有了更接近人类正常访问方式的页面爬取方式（于是有了`htsamc_h`爬虫）
	
* 第二处改进是优化了代码，减少冗余，特别是在`DateProcessorPipeline`中将原来的返回空字典变成抛出`DropItem`异常，以更具`Scrapy`风格的方式结束`item`传递

* 第三处改进是随机更换每次请求时头部信息中的`UserAgent`，使用`fake-useragent`包进行处理；不过在每隔较长一段时间后首次执行爬虫会出现`fake-useragent`更新`ua`库失败的报错信息，但是使用本地缓存的`ua`信息是没问题的（再次启动爬虫就不会再报错），所以就目前而言没有太大影响

* 第四处改进是完成了代码编写，却实际并没有运用；这一块就是代理（`proxy`）的设置；使用`Requests`包以及`Scrapy`中的`Selector`进行了对[西刺代理（国内高匿代理）](http://www.xicidaili.com/nn)的爬取，将获得`ip`等相关信息存入了`Json`文件，之后通过爬虫`middleware`读取`Json`文件随机获取代理`ip`进行网页请求，但是结果显示大量的`ip`被目标网页拒绝，为了节约时间便搁置了设置代理的操作
