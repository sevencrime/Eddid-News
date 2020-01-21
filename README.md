安装 virtualenv
pip install virtualenv -i https://pypi.douban.com/simple

cd WORKdir

在当前目录下创建一个名叫 env 的目录（虚拟环境）
virtualenv venv

安装依赖
venv\Scripts\pip install -r requirements.txt --index-url https://pypi.douban.com/simple

windows进入虚拟环境：进入到虚拟环境的scripts文件夹中，然后执行activate
linux 激活虚拟环境: source bin/activate

退出虚拟环境很简单，通过一个命令就可以完成：deactivate