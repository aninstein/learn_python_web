---
title:  Nginx学习笔记-基础篇
tags: nginx,中间件,基础篇
grammar_abbr: true
grammar_table: true
grammar_defList: true
grammar_emoji: true
grammar_footnote: true
grammar_ins: true
grammar_mark: true
grammar_sub: true
grammar_sup: true
grammar_checkbox: true
grammar_mathjax: true
grammar_flow: true
grammar_sequence: true
grammar_plot: true
grammar_code: true
grammar_highlight: true
grammar_html: true
grammar_linkify: true
grammar_typographer: true
grammar_video: true
grammar_audio: true
grammar_attachment: true
grammar_mermaid: true
grammar_classy: true
grammar_cjkEmphasis: true
grammar_cjkRuby: true
grammar_center: true
grammar_align: true
grammar_tableExtra: true
--- 
---

* [1. nginx优势](#1-nginx优势)
	* [1.1 nginx实现了IO流多路复用](#11-nginx实现了io流多路复用)
		* [1.1.1 select](#111-select)
		* [1.1.2 poll](#112-poll)
		* [1.1.3 epoll](#113-epoll)
		* [1.2 nginx是轻量级的](#12-nginx是轻量级的)
	* [1.3 nginx和CPU亲和](#13-nginx和cpu亲和)
	* [1.4 sendfile](#14-sendfile)
* [2. 快速安装](#2-快速安装)
* [3. Nginx基本参数配置](#3-nginx基本参数配置)
	* [3.1 安装目录](#31-安装目录)
	* [3.2 Nginx的配置参数说明](#32-nginx的配置参数说明)
* [4 Nginx简单配置demo](#4-nginx简单配置demo)
	* [4.1 配置主页](#41-配置主页)

---
## 1. nginx优势
### 1.1 nginx实现了IO流多路复用
多个[描述符](https://baike.baidu.com/item/%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6/9809582?fr=aladdin)的I/O都能够在一个线程内交替并发地顺序完成，这个“复用”实际上是对同一个线程的复用，这个就是I/O多路复用。
```sequence
Note left of 应用: Block
应用->内核: Read请求可用
Note right of 内核: 初始化I/O数据拷贝
内核-->应用: Read完成
```
I/O多路复用实现，在linux上的实现方式主要包括：**select，epoll**
#### 1.1.1 select
select会不断的依次的循环Block队列中的内容，效率低下，而且对文件描述符会有限制
- 能够监视文件描述符的数量存在最大限制，只有1024个[【相关链接】](https://blog.csdn.net/j6915819/article/details/81015434)
- 线性扫描效率低下

#### 1.1.2 poll
本质上和select没有区别，只是没有了最大连接数的限制

#### 1.1.3 epoll
- 当每一个FD（文件描述符）就绪的时候，采用系统回调函数之间，将FD放入，效率更高
- 没有最大连接数限制

#### 1.2 nginx是轻量级的
- 功能模块化
- 代码模块化

### 1.3 nginx和CPU亲和
nginx使用worker对CPU进行绑定，是一种把CPU核心和Nginx工作进程绑定方式，把每个worker进程固定在一个CPU上执行，减少切换CPU的cache miss，获得更好的性能

### 1.4 sendfile
当我们请求一个文件的时候，在内核工作的时候：**内核空间->用户空间->socket给client**
但是在nginx里面，由于静态文件不需要经过用户空间进行逻辑处理，所以是直接：**内核空间->socket了**
```sequence
file->Kernel space: Buffer cache
Kernel space->User space: Buffer cache
User space->Socket: Buffer cache
Kernel space->Socket: (Nginx)Buffer cache
Note right of Socket: 给客户端
```
## 2. 快速安装
确认环境：
1. centos7.0以上
2. 能够连接公网
3. 能够使用yum，pip
4. 关闭iptables和selinux


安装编译环境：
```shell
yum install -y gcc gcc-c++ autoconf pcre pcre-devel make automake
```
安装常用工具：
```shell
yum install -y wget httpd-tools vim
```
初始化自己的环境文件夹：
```shell
cd /<mydir> 
mkdir app download logs work backup
# app 代码目录
# download 下载的依赖
# logs 日志文件
# work 一些shell脚本
# backup 备份的配置文件
```

在nginx官方网站上找到centos的yum源
```
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
```

在centos上安装yum repo
1. 需要在**/etc/yum.repos.d/**文件夹下新建一个yum repo文件**nginx.repo**，并且把上述的yum源配置上去
```shell
touch /etc/yum.repos.d/nginx.repo
vim /etc/yum.repos.d/nginx.repo  # 然后把上面的yum源粘贴上去
```

粘贴的yum源还需要改动os和版本，所以实际上应该粘贴的内容是，然后保存即可。
```
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/8/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
```

默认情况下，使用稳定nginx包的存储库。如果您想使用主线nginx包，请运行以下命令
```
sudo yum-config-manager --enable nginx-stable
```

然后就可以试试，使用**yum list|grep nginx**可以看到已经有nginx的安装内容
```linux
[root@centos8 ~]# yum list|grep nginx
Repository AppStream is listed more than once in the configuration
Repository extras is listed more than once in the configuration
Repository PowerTools is listed more than once in the configuration
Repository centosplus is listed more than once in the configuration
nginx.x86_64                                         1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-all-modules.noarch                             1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-debuginfo.x86_64                               1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-filesystem.noarch                              1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-mod-http-image-filter.x86_64                   1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-mod-http-perl.x86_64                           1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-mod-http-xslt-filter.x86_64                    1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-mod-mail.x86_64                                1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-mod-stream.x86_64                              1:1.14.1-9.module_el8.0.0+184+e34fea82            AppStream        
nginx-module-image-filter.x86_64                     1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-module-image-filter-debuginfo.x86_64           1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-module-njs.x86_64                              1:1.18.0.0.4.3-1.el8.ngx                          nginx-stable     
nginx-module-njs-debuginfo.x86_64                    1:1.18.0.0.4.3-1.el8.ngx                          nginx-stable     
nginx-module-perl.x86_64                             1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-module-perl-debuginfo.x86_64                   1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-module-xslt.x86_64                             1:1.18.0-1.el8.ngx                                nginx-stable     
nginx-module-xslt-debuginfo.x86_64                   1:1.18.0-1.el8.ngx                                nginx-stable     
pcp-pmda-nginx.x86_64                                5.0.2-5.el8                                       AppStream  v
```

然后安装nginx
```
sudo yum install nginx
```

## 3. Nginx基本参数配置
### 3.1 安装目录
通过yum安装的都是rpm包，所以可以通过查看安装目录
```shell
rpm -ql nginx
```
可以得到以下结果
```linux
[root@centos8 ~]# rpm -ql nginx
/etc/logrotate.d/nginx
/etc/nginx
/etc/nginx/conf.d
/etc/nginx/conf.d/default.conf
/etc/nginx/fastcgi_params
/etc/nginx/koi-utf
/etc/nginx/koi-win
/etc/nginx/mime.types
/etc/nginx/modules
/etc/nginx/nginx.conf
/etc/nginx/scgi_params
/etc/nginx/uwsgi_params
/etc/nginx/win-utf
/etc/sysconfig/nginx
/etc/sysconfig/nginx-debug
/usr/lib/.build-id
/usr/lib/.build-id/72
/usr/lib/.build-id/72/32b3d274d95e3739c1690a6344d3aac4c6272b
/usr/lib/.build-id/7f
/usr/lib/.build-id/7f/0259e101e7ab850dee7e6ac2907ac62f6f5917
/usr/lib/systemd/system/nginx-debug.service
/usr/lib/systemd/system/nginx.service
/usr/lib64/nginx
/usr/lib64/nginx/modules
/usr/libexec/initscripts/legacy-actions/nginx
/usr/libexec/initscripts/legacy-actions/nginx/check-reload
/usr/libexec/initscripts/legacy-actions/nginx/upgrade
/usr/sbin/nginx
/usr/sbin/nginx-debug
/usr/share/doc/nginx-1.18.0
/usr/share/doc/nginx-1.18.0/COPYRIGHT
/usr/share/man/man8/nginx.8.gz
/usr/share/nginx
/usr/share/nginx/html
/usr/share/nginx/html/50x.html
/usr/share/nginx/html/index.html
/var/cache/nginx
/var/log/nginx
[root@centos8 ~]#
```
简单来看，主要分为三部分目录
- /etc目录，主要是放一些核心额配置
- /usr目录
- /var目录

对于Nginx的安装目录，rpm包规范配置：
|   路径  |  类型   |  作用   |
| --- | --- | --- |
|/etc/logrotate.d/nginx  |  配置文件   |   Nginx日志轮转，用于logrotate服务的日志切割  |
|/etc/nginx<br>/etc/nginx/nginx.conf<br>/etc/nginx/conf.d<br>/etc/nginx/conf.d/default.conf   |  目录、配置文件   |  Nginx主配置文件   |
|/etc/nginx/fastcgi_params<br>/etc/nginx/scgi_params<br>/etc/nginx/uwsgi_params   |  配置文件   |   cgi配置相关，fastcgi配置  |
|/etc/nginx/koi-utf<br>/etc/nginx/koi-win<br>/etc/nginx/win-utf|配置文件 |编码转换映射转化文件|
|/etc/nginx/mime.types|配置文件|设置http协议的Content-Type与拓展名对应关系|
|/usr/lib/systemd/system/nginx-debug.service<br>/usr/lib/systemd/system/nginx.service<br>/etc/sysconfig/nginx<br>/etc/sysconfig/nginx-debug|配置文件|用于配置出系统守护进程管理器管理方式|
|/usr/lib64/nginx/modules<br>/etc/nginx/modules|目录|Nginx模块目录|
|/usr/sbin/nginx<br>/usr/sbin/nginx-debug|命令|Nginx服务的启动管理终端命令|
|/usr/share/doc/nginx-1.18.0<br>/usr/share/doc/nginx-1.18.0/COPYRIGHT<br>/usr/share/man/man8/nginx.8.gz|文件、目录|Nginx的手册和帮助文档|
|/var/cache/nginx|目录|Nginx缓存目录|
|/var/log/nginx|目录|Nginx的日志目录|

### 3.2 Nginx的配置参数说明
终端输入
```
nginx -V  # 大写V
```
输出配置
```linux
[root@centos8 ~]# nginx -V
nginx version: nginx/1.18.0
built by gcc 8.3.1 20190507 (Red Hat 8.3.1-4) (GCC) 
built with OpenSSL 1.1.1c FIPS  28 May 2019
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules \
--conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log  \
--http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock \ 
--http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp \ 
--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \ 
--http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads \ 
--with-http_addition_module --with-http_auth_request_module --with-http_dav_module \
--with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module \ 
--with-http_mp4_module --with-http_random_index_module --with-http_realip_module \
--with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module \
--with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream \
--with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module \
--with-cc-opt='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -fPIC' \ 
--with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie'
[root@centos8 ~]#
```
从上面的配置，那些“--with”的，除了--with-cc-opt其他都不做说明

|编译选项 |说明 |配置方式|
| --- | --- | --- |
|--prefix=/etc/nginx|Nginx主目录|在安装编译的时候产生|
|--sbin-path=/usr/sbin/nginx|Nginx执行命令|在安装编译的时候产生|
|--modules-path=/usr/lib64/nginx/modules|Nginx模块目录|在安装编译的时候产生|
|--conf-path=/etc/nginx/nginx.conf|Nginx配置文件|在安装编译的时候产生|
|--error-log-path=/var/log/nginx/error.log|Nginx错误日志|在安装编译的时候产生|
|--http-log-path=/var/log/nginx/access.log|Nginx访问日志|在安装编译的时候产生|
|--pid-path=/var/run/nginx.pid|Nginx的pid文件，记录了这个Nginx服务启动的pid| 在安装编译的时候产生|
|--lock-path=/var/run/nginx.lock |Nginx锁|在安装编译的时候产生|
|http-client-body-temp-path=/var/cache/nginx/client_temp<br>--http-proxy-temp-path=/var/cache/nginx/proxy_temp<br>--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp<br> --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp<br>--http-scgi-temp-path=/var/cache/nginx/scgi_temp|缓存目录，执行对应模块的时候Nginx产生的临时保留文件|-|
|--user=ngin<br>--group=nginx|设定Nginx启动的用户和用户组，我们虽然使用root启动的Nginx但是实际上的Nginx的Worker是在nginx指定的用户上去跑的|-|
|--with-cc-opt |设置额外的参数将被添加到CFLAGS变量当中|-|
|--with-ld-opt |设置附加的参数，链接系统库|-|


## 4 Nginx简单配置demo
### 4.1 配置主页
Nginx的配置文件主要是/etc/nginx/nginx.conf和/etc/nginx/conf.d/default.conf配置文件，当Nginx启动的时候会先加载nginx.conf，再加载default.conf中的配置。
在default.conf中配置的server选项中可以配置index.html页面，在location选项里面可以配置主页的路径和地址
```python
server {
    listen       80;
    server_name  192.168.0.1;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /myproject/static;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root  /myproject/static;
    }
}
```
完成配置的更改后，可以使用systemctl启动nginx
```linux
systemctl start nginx
```

当nginx配置文件更改的时候，可以使用reload更新配置，也可以选择重启nginx
```linux
systemctl reload nginx
systemctl restart nginx
```

当然也有tc工具可以校验nginx配置文件正确性
命令：
```linux
nginx -tc nginx.conf
```
输出：
```linux
[root@centos8 nginx]# nginx -tc nginx.conf 
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
[root@centos8 nginx]#
```