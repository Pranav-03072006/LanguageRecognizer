"""
Vercel Serverless Function entry point for Django WSGI application.
"""
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure VERCEL environment flag and settings module are set
os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
django.setup()

# Auto-migrate SQLite in serverless temp directory if database does not exist
if os.getenv("VERCEL") == "1" and not os.getenv("DATABASE_URL"):
    import tempfile
    from django.core.management import call_command
    db_path = Path(tempfile.gettempdir()) / "db.sqlite3"
    if not db_path.exists():
        try:
            call_command("migrate", interactive=False)
        except Exception as exc:
            print("Vercel auto-migration notice:", exc)

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
app = application
