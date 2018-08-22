# htsamc-Spider

### 基本情况

* 通过`chrome`浏览器开发者工具分析网页，发现可以直接在未登录状态下获取公告页中各公告名字和`PDF`下载链接；但是却无法获得当前具体的页数（页数信息不是静态的），所以如果直接将该页面设为爬虫入口，则最多只能爬取1页

* 继续通过浏览器开发者工具进行分析，发现当进行翻页操作时，本地会想服务器发送一个请求，该请求的URL非常具有特征性: *http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage=10* 尝试将`rowOfPage`参数进行修改就会发现页面会跳转到显示相应数量公告的页面；于是只要在浏览器中看到总共有几页，在进行计算获得总共的公告数量，就能通过修改`rowOfPage=总数`进行所有公告的获取和下载

* 在进行代码编写时，为了节约资源以及公告文件时效性，于是通过对网页上每个公告创建时间的判读，每次爬取只下载离爬取日期两周的文件，在数据储存上并不区分时效而是将所有公告进行信息存储

	* 根据公告时间选择性下载的实现，主要是通过不同`pipelines`之间传递`item`实现,在用于下载的`MyFilesPipeline`前一个`DateProcessorPipeline`处理`item`时，如果其中的`is_recent`属性为`False`，那么就返回空字典`{}`，这样下一个`pipeline`也无法处理

	* 这次爬虫最终数据计划是存储在`CSV`文件中，存储过程使用了`scrapy.exporters`模块中的`CsvItemExporter`类,通过阅读文档了解了这个类的使用方法，最终存储成功

	* `MyFilesPipeline`继承了`Scrapy`默认的`FilesPipeline`类，通过重写`item_completed`与`item_completed`方法修改了保存下载后`PDF`的名字和用于保存的文件夹名字

	* 以上基本达成最初爬虫目的


### 完成改进

* 最大的改进：为了进一步自动化爬取，意图通过程序获得网页中公告的总页数，然后实现分页爬取

* 运用了Selenium进行模拟请求网页，获得完整的页面并通过`css`解析获得总页数，之后通过字符串的`format`方法对`rowOfPage`进行修改逐页进行请求

* 第二处改进是优化了代码，减少冗余，特别是在`DateProcessorPipeline`中将原来的返回空字典变成抛出`DropItem`异常，以更具`Scrapy`风格的方式结束`item`传递
