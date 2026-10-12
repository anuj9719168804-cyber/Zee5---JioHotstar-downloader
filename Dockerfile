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
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY Requirements.txt /app/Requirements.txt
RUN pip3 install --no-cache-dir -r /app/Requirements.txt

COPY . /app/

# Run the script through bash to avoid exec-format errors from missing shebang
# or Windows CRLF line endings.
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]
