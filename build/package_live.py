"""Packages the official website for www.mbusoms.co.za.

    python3 build/package_live.py

Copies site/, rebuilds every page in live mode (indexable, canonical URLs, sitemap,
search-friendly robots.txt), and writes dist/mbusoms-live/ plus a zip ready to upload
into public_html. The GitHub Pages preview stays hidden from search engines."""
import os, shutil, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "mbusoms-live"
ZIP = ROOT / "dist" / "mbusoms-live-upload.zip"

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(ROOT / "site", OUT, ignore=shutil.ignore_patterns(".nojekyll", "_headers", "*.bak"))
env = dict(os.environ, MBUSO_LIVE="1", MBUSO_OUT=str(OUT))
subprocess.run([sys.executable, str(ROOT / "build" / "build.py")], env=env, check=True, stdout=subprocess.DEVNULL)
shutil.copy(ROOT / "UPLOAD-GUIDE.md", OUT / "UPLOAD-GUIDE.md")

ZIP.unlink(missing_ok=True)
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(OUT))
print(f"live site: {OUT}\nupload zip: {ZIP} ({ZIP.stat().st_size // 1024} KB)")
