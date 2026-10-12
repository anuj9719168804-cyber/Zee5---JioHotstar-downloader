FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# The repository file is named Requirements.txt (capital R).
COPY Requirements.txt /app/Requirements.txt
RUN pip3 install --no-cache-dir -r /app/Requirements.txt

COPY . /app/

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
