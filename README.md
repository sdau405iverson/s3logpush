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
        git checkout logBackServer
#### 2. 配置修改
        vi s3logpush/s3logpush/config.py
        
        #aws_access_key_id
        #aws_secret_access_key
        #endpoint_url -->S3访问地址
        S3_CONNECT = {'aws_access_key_id': 'EPB64269G0R8YXJRVXST',
                      'aws_secret_access_key': 'gHM03TgOTlhALuMqCGDtCtHZR1WGaLOuorxeyB3U',
                      'endpoint_url': 'http://192.168.3.238:8888'}
        #日志备份的根目录
        BASE_DIR = '/jboss/otswslog'

        #日志备份根目录下以IP地址命名的所有目录
        IP_ADDRS = [
        '10.2.201.10',
        '10.2.201.11',
        '10.2.201.12',
        ]
        #备份日志根目录下所有的服务分组
        SERVERS = [
            #name: 服务分组名称
            #ports:该分组下的所有端口
            #log_name_format: 服务分组对应所有日志格式
            {'name': 'login',
             'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
             'log_name_format': ['server.log.%Y-%m-%d-%H',
                                 'bindLogger.log.%Y-%m-%d-%H',
                                 'loginrecord.log.%Y-%m-%d-%H',
                                 'sp.log.%Y-%m-%d-%H'
                                 ],
             'bucket': 'partition3'
             },
            {'name': 'pay',
             'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
             'log_name_format': ['server.log.%Y-%m-%d-%H',
                                 'ccos.log.%Y-%m-%d-%H',
                                 'passenger_redis.log.%Y-%m-%d-%H',
                                 'sp.log.%Y-%m-%d-%H',
                                 'innercallback.log.%Y-%m-%d-%H',
                                 'httpnotify.log.%Y-%m-%d-%H'
                                 ],
             'bucket': 'partition3'
             },
        ]
        
            
        #log_directory --> 待上传日志的存放目录
        #name --> 待上传日志的名称（时间戳部分需要使用pythond的datetime format）
        #bucket --> 日志上传的目标bucket,bucket必须已存在
        APP_LOG_INFOS = []
        
        
        #上传线程的并发数
        PARALLEL_NUM = 3
        # 定时任务执行时间定义
        SCHEDULER = {'hour': '0-23', 'minute': '5'}
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
            startstop.sh的同级目录下s3logpush_run.log
        * 错误日志
            startstop.sh的同级目录下s3logpush_error.log

**注意：**
    如果不需要执行定时收集日志的任务，只需将s3logpush/s3logpush/s3logpush.py末尾的如下行进行注释
    
    #sched = Scheduler(daemonic=False)
    #sched.start()
    #sched.add_cron_job(producer, args=(log_collectors,), **config.SCHEDULER)
    