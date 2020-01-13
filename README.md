安装 virtualenv
pip install virtualenv -i https://pypi.douban.com/simple

cd dir

在当前目录下创建一个名叫 env 的目录（虚拟环境）
virtualenv env
(出现 virtualenv command not found  :  ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv)

启动虚拟环境
cd ENV
source ./bin/activate

退出虚拟环境
deactivate