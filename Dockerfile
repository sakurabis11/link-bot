FROM python:3.10
RUN apt update && apt upgrade -y && apt install gcc  ffmpeg python3 python3-pip -y
RUN apt install git -y
RUN pip install --upgrade pip

RUN pip install pafy
RUN pip install aiohttp
RUN pip install pymongo

COPY requirements.txt /requirements.txt

RUN cd /
RUN pip install -U pip && pip install -U -r requirements.txt
WORKDIR /app

COPY . .
CMD ["python3", "bot.py"]
