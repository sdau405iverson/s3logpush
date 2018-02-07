 S3日志上传使说明
 ==============

> * 目标：将本地日志上传至S3服务
> * 日志搜集： 定时收集本地日志目录新增日志文件
> * 日志上传：如果S3服务器已经存在且大小与本地文件一致则不会上传，否上传本地文件

### *前提*
> * 本地服务器正确配置了ip地址，也就是能够通过hostname -i获取ip地址（且结果不能是127.0.0.1）

### 使用方法
#### 1. clone代码
        git clone https://github.com/sdau405iverson/s3logpush.git
        git checkout master
#### 2. 配置修改
        vi s3logpush/s3logpush/config.py
        ```
        #aws_access_key_id
        #aws_secret_access_key
        #endpoint_url -->S3访问地址
        S3_CONNECT = {'aws_access_key_id': 'EPB64269G0R8YXJRVXST',
                      'aws_secret_access_key': 'gHM03TgOTlhALuMqCGDtCtHZR1WGaLOuorxeyB3U',
                      'endpoint_url': 'http://192.168.3.238:8888'}

        #log_directory --> 待上传日志的存放目录
        #bucket --> 日志上传的目标bucket,bucket必须已存在
        APP_LOG_INFOS = [
            {'log_directory': '/home/samsing/pythonProjects/supersets','bucket': 'testdata'},
        ]
        #上传线程的并发数
        PARALLEL_NUM = 3
        # 定时任务执行时间定义
        SCHEDULER = {'hour': '0-23', 'minute': '5'}
        ```
> 参考：
> [dateformat](https://www.cnblogs.com/guigujun/p/6149770.html)

### 3. 执行
        * 启动
            进入startstop.sh所在目录，然后执行如下命令
            ./startstop.sh start
        * 停止
            ./startstop.sh stop
        * 查看状态
            ./startstop.sh status
**注意：logCollector/tcollector/collectors/1/s3logpush_run.py 必须有执行权限**

### 4. 查看日志
        * 执行日志
            startstop.sh同级目录下的s3logpush_run.log
        * 错误日志
           startstop.sh同级目录下的s3logpush_error.log 