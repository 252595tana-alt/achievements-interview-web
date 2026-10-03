"""Build the self-contained editable HTML. No external Python packages are required."""
from pathlib import Path
import base64
root = Path(__file__).resolve().parent
css = (root / "styles.css").read_text(encoding="utf-8")
for filename, mime in (("background-cover.webp", "image/webp"), ("background-body.webp", "image/webp")):
    path = root / "assets" / filename
    css = css.replace("assets/" + filename, "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii"))
js = (root / "script.js").read_text(encoding="utf-8")
if "</script" in js.lower():
    raise ValueError("script.js contains an unexpected HTML script terminator")
shell = (root / "shell.html").read_text(encoding="utf-8")
result = shell.replace("__STYLES__", "<style>\n" + css + "\n</style>").replace("__SCRIPT__", "<script>\n" + js + "\n</script>")
(root / "index.html").write_text(result, encoding="utf-8")
print("Built index.html:", len(result.encode("utf-8")), "bytes")
