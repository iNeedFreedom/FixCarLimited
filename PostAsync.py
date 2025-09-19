from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Your GitHub config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "YOUR_GITHUB_PAT"
OWNER = "iNeedFreedom"
REPO = "FixCarLimited"
FILE_PATH = "Data.js"

# Get file info from GitHub (sha required for updates)
def get_file_info():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "Python-App"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Failed to fetch file:", resp.text)
        return None

@app.route("/roblox", methods=["POST"])
def roblox_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # Encode new JSON content
    new_content = base64.b64encode(
        bytes(str(data).replace("'", '"'), "utf-8")
    ).decode("utf-8")

    # Get current sha
    file_info = get_file_info()
    if not file_info:
        return jsonify({"error": "Could not fetch file"}), 500

    sha = file_info["sha"]

    # Prepare request body
    body = {
        "message": "Update Data.js from Roblox",
        "content": new_content,
        "sha": sha
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "Python-App",
        "Content-Type": "application/json"
    }

    resp = requests.put(url, json=body, headers=headers)

    if resp.status_code in [200, 201]:
        return jsonify({"status": "success", "github": resp.json()})
    else:
        return jsonify({"error": resp.text}), resp.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
