from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os, json, secrets, string
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret"

DATA_FILE = "urls.json"

def load_data():
    """Load mappings from JSON file (create empty file if missing)."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_code(length=6):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def ensure_unique_code(data, length=6):
    while True:
        c = generate_code(length)
        if c not in data:
            return c

def normalize_url(url):
    url = url.strip()
    # if no scheme, add http:// so redirect works
    if not urlparse(url).scheme:
        return "http://" + url
    return url

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    short_url = None

    if request.method == "POST":
        long_url = request.form.get("long_url", "").strip()
        custom_alias = request.form.get("custom_alias", "").strip()

        if not long_url:
            flash("Please enter a URL.", "danger")
            return redirect(url_for("index"))

        long_url = normalize_url(long_url)

        # If custom alias provided, ensure it's not taken and is valid
        if custom_alias:
            if custom_alias in data:
                flash("Alias already taken. Pick another one.", "danger")
                return redirect(url_for("index"))
            code = custom_alias
        else:
            code = ensure_unique_code(data)

        data[code] = {"url": long_url, "clicks": 0}
        save_data(data)

        short_url = request.host_url + code  # e.g. http://127.0.0.1:5000/abc123

    return render_template("index.html", short_url=short_url)

@app.route("/<string:code>")
def redirect_short(code):
    data = load_data()
    if code in data:
        # increment clicks
        data[code]["clicks"] = data[code].get("clicks", 0) + 1
        save_data(data)
        return redirect(data[code]["url"])
    else:
        flash("Short link not found.", "warning")
        return redirect(url_for("index"))

@app.route("/list")
def list_links():
    data = load_data()
    # sort by clicks descending for convenience
    sorted_items = sorted(data.items(), key=lambda kv: kv[1].get("clicks", 0), reverse=True)
    return render_template("list.html", items=sorted_items, host=request.host_url)

@app.route("/api/links")
def api_links():
    """Simple JSON API to view all links."""
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(debug=True)
