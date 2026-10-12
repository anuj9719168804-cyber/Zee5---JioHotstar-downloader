
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pyrogram
from config import Config

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("Zee5Bot")
logging.getLogger("pyrogram").setLevel(logging.INFO)

# Render health server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Zee5 Telegram Bot is running"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.environ.get("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server.daemon_threads = True

    thread = threading.Thread(
        target=server.serve_forever,
        name="health-server",
        daemon=True,
    )
    thread.start()
    logger.info("Health server listening on port %s", port)


def main():
    # Health endpoint starts before the Telegram client.
    start_health_server()

    download_path = Path(Config.DOWNLOAD_LOCATION)
    download_path.mkdir(parents=True, exist_ok=True)

    plugin_path = Path(__file__).resolve().parent / "plugins"
    if not plugin_path.is_dir():
        logger.error("Plugins folder is missing: %s", plugin_path)
    else:
        plugin_files = list(plugin_path.glob("*.py"))
        plugin_files = [
            p for p in plugin_files if p.name != "__init__.py"
        ]
        if not plugin_files:
            logger.warning(
                "No top-level Python plugin files found in %s",
                plugin_path,
            )
        else:
            logger.info(
                "Plugin files found: %s",
                ", ".join(p.name for p in plugin_files),
            )

    app = pyrogram.Client(
        "Zee5",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins={"root": "plugins"},
    )

    if hasattr(Config, "AUTH_USERS"):
        Config.AUTH_USERS.add(680815375)

    logger.info("Starting Telegram bot...")
    try:
        app.run()
    except Exception:
        logger.exception("Telegram bot stopped because of an error")
        raise


if __name__ == "__main__":
    main()
