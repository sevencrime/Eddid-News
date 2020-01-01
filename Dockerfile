FROM selenium/hub

# RUN docker stop $(docker ps -a |  grep "selenium*"  | awk '{print $1}')
# RUN docker rm $(docker ps -a |  grep "selenium*"  | awk '{print $1}')
RUN docker rm 80f8c3892376

# 启动主hub容器
RUN docker run -d -p 32777:4444 --name selenium-hub selenium/hub

FROM selenium/node-chrome

# RUN docker stop $(docker ps -a |  grep "selenium*"  | awk '{print $1}')
# RUN docker rm $(docker ps -a |  grep "selenium*"  | awk '{print $1}')

# 启动分支node chrome 容器
RUN docker run -d --link selenium-hub:hub selenium/node-chrome



# 基于python3.6.8镜像
FROM python:3.6.8

LABEL onedi="onedi@qq.com"

# 更新pip
RUN pip install --upgrade pip --index-url https://pypi.douban.com/simple

# 工作目录
WORKDIR /Eddid-News
ADD . /Eddid-News

# pip安装依赖包
RUN pip install -r requirements.txt --index-url https://pypi.douban.com/simple

# 传递参数
ENTRYPOINT ["python"]

# 默认显示help帮助信息
CMD ["--help"]
