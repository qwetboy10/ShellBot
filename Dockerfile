FROM ubuntu:18.04


RUN apt-get update
RUN apt-get install -y python3 python3-pip sudo
RUN pip3 install discord.py requests


RUN useradd -ms /bin/bash bot
RUN usermod -aG sudo bot
RUN echo 'bot:password123' | chpasswd
USER bot

COPY . /home/bot/.app
WORKDIR /home/bot/.app

CMD ["python3", "bot.py"]
