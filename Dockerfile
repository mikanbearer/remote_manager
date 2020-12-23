FROM python:3.8.4
RUN mkdir -p /demo
ADD requirements.txt /demo
WORKDIR /demo
RUN pip3 install -r requirements.txt
RUN git clone https://github.com/novnc/websockify /websockify
RUN git clone https://github.com/novnc/noVNC /static/noVNC