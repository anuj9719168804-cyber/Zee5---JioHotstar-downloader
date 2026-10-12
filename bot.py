import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from pyrogram import Client
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Zee5Bot")
logging.getLogger("pyrogram").setLevel(logging.INFO)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Zee5 Telegram Bot health endpoint is online"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
    def log_message(self, fmt, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    threading.Thread(target=server.serve_forever, daemon=True, name="health-server").start()
    logger.info("Health server listening on port %s", port)

def main():
    missing = []
    if not Config.TG_BOT_TOKEN: missing.append("TG_BOT_TOKEN")
    if not Config.APP_ID: missing.append("APP_ID")
    if not Config.API_HASH: missing.append("API_HASH")
    if missing:
        raise RuntimeError("Missing required Render environment variables: " + ", ".join(missing))

    start_health_server()
    Path(Config.DOWNLOAD_LOCATION).mkdir(parents=True, exist_ok=True)
    plugin_dir = Path(__file__).resolve().parent / "plugins"
    plugin_files = [p.name for p in plugin_dir.glob("*.py") if p.name != "__init__.py"]
    logger.info("Plugin files found: %s", ", ".join(sorted(plugin_files)) or "NONE")

    app = Client(
        "Zee5", bot_token=Config.TG_BOT_TOKEN, api_id=Config.APP_ID, api_hash=Config.API_HASH,
        plugins={"root": "plugins"},
    )
    # Preserve the owner ID, and allow additional IDs from AUTH_USERS.
    Config.AUTH_USERS.add(680815375)
    logger.info("Starting Telegram bot...")
    app.run()

if __name__ == "__main__":
    main()
