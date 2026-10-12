
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git python3 python3-pip ffmpeg bash ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY Requirements.txt /app/Requirements.txt
RUN pip3 install --no-cache-dir -r /app/Requirements.txt

COPY . /app/

RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

EXPOSE 10000

CMD ["bash", "/app/start.sh"]
