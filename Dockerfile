FROM python:3.7

# set display port to avoid crash
# News Spider
ENV DISPLAY=:105

# copy unibit scrapy file
COPY . .

# install requirements
RUN pip3 install -r requirements.txt

# Company Financial Quarterly
CMD ./run_news_spider.sh