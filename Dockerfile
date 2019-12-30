FROM selenium/hub

FROM selenium/node-chrome

# 基于python3.6.8镜像
FROM python:3.6.8

MAINTAINER onedi  <onedi@qq.com>

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

