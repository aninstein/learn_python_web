# flask学习笔记
---
---
## 1. 搭建环境
### 1.1 虚拟环境（使用==pipenv==）
使用pipenv搭建虚拟环境，来代替原来的virtualenv+requirement.txt的方式，完成虚拟环境的搭建。
在项目的根目录，安装虚拟环境命令，随后会生成==Pipfile==：
```
pip install pipenv
```
执行命令之后，在会在~/.local/share/virtualenvs/目录下创建虚拟环境文件夹

- ==pipenv install== 创建虚拟环境
- ==pipenv shell== 显示激活虚拟环境
- ==pipenv run== 如pipenv run python hello.py，可以用虚拟环境运行hello.py
- 与传统的requirement.txt手动维护的依赖包不同，pipenv在install之后会产生一个Pipfile文件
- ==pipenv graph== 查看依赖情况
- ==pipenv install \<pkg>== 安装pip包到虚拟环境，可以使用此命令安装flask：==pipenv install flask==
- ==pipenv update== 更新python包
## 2. hello world
1. ==@route()== 方法介绍
2. 
## 3. 登陆页面
## 4. 表单验证
## 5. 前后台交互
## 6. mysql数据集合
## 7. 安全能力
## 8. 部署方式
## 9. 高可用
## 10. 可视化