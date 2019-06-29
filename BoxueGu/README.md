# 连猴子都看得懂的操作流程

##### 1. 进入ubuntu系统，在桌面上建立一个仓库文件夹

```shell
cd Desktop
mkdir git
```

##### 2. 进入终端bash shell，进入仓库文件夹，克隆远程仓库

```shell
cd git
git init
git clone git@gitee.com:python_commando/BoxueGu.git
```

##### 3. 进入自己的分支 

```shell
git checkout -b Pengbiaobiao
# 将Pengbiaobiao换为自己的名字
# Hanhaichuan	韩海川
# Jingxingwei	景星微
# Kongyue		孔越
# Xuliuxiang	徐刘祥
# Yuanmo		袁墨
```

> master分支已被锁定，进入自己的分支操作

##### 4. 测试仓库

修改README文件并推送到自己的分支

```
# 由于gitee组织仓库只支持五个人协同编辑，提交代码的时候使用统一的账号密码
# 账号：coder_eraser
# 密码：chuanzhi315
```

如果遇到如下提示：

```
warning: push.default 尚未设置，它的默认值在 Git 2.0 已从 'matching'
变更为 'simple'。若要不再显示本信息并保持传统习惯，进行如下设置：

  git config --global push.default matching

若要不再显示本信息并从现在开始采用新的使用习惯，设置：

  git config --global push.default simple

当 push.default 设置为 'matching' 后，git 将推送和远程同名的所有
本地分支。

从 Git 2.0 开始，Git 默认采用更为保守的 'simple' 模式，只推送当前
分支到远程关联的同名分支，即 'git push' 推送当前分支。

参见 'git help config' 并查找 'push.default' 以获取更多信息。
（'simple' 模式由 Git 1.7.11 版本引入。如果您有时要使用老版本的 Git，
为保持兼容，请用 'current' 代替 'simple'）
```

输入：`git config --global push.default simple`

##### 5. 建立虚拟环境

```shell
mkvirtualenv -p python3 boxuegu
```

##### 6. 安装环境

把下发的项目文件夹里的requirements.txt复制到ubuntu项目目录下，然后执行以下代码

```shell
pip install -r requirements.txt
```

##### 7. 设置pycharm相应环境

设置setting -> project interpreter 设置你当前虚拟环境的编译器

设置version control 为当前git 

##### 8、安装xadmin模块

```shell
# 该模块需要单独安装
pip install https://github.com/sshwsfc/xadmin/tarball/master
```

##### 9、创建数据

```mssql
create database boxuegu charset=utf8;
```

##### 10、迁移数据库

```shell
# 已经有迁移文件,可以直接进行迁移
python manage.py migrate
```

##### 11、运行项目

```shell
python manage.py runserver
```

##### 12、创建超级管理用用户

```shell
python mamage.py createsuperuser
```

##### 13、登录admin

```html
127.0.0.1:8000/admin
```

​	









