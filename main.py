from flask import Flask
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_trending():
    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"

    try:
        response = requests.get(
            url,
            headers={
                "Accept": "application/vnd.github+json"
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get("items", [])

    except Exception:
        pass

    return []


def analyze_repo(repo_name, description):

    if not GEMINI_API_KEY:
        return "❌ GEMINI_API_KEY 未設定"

    prompt = f"""
你是一位創業分析師。

分析這個專案：

名稱:
{repo_name}

描述:
{description}

請輸出：

需求度(0-100)
競爭度(0-100)
變現度(0-100)
開發難度(0-100)

最後給一句商機評價。
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        r = requests.post(
            url,
            json=payload,
            timeout=60
        )

        if r.status_code != 200:
            return f"❌ Gemini API 錯誤<br><pre>{r.text}</pre>"

        data = r.json()

        if "candidates" not in data:
            return f"❌ Gemini 回傳異常<br><pre>{r.text}</pre>"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Exception<br><pre>{str(e)}</pre>"


@app.route("/")
def home():

    repos = get_trending()

    if not repos:
        return "<h1>❌ 無法取得 GitHub 資料</h1>"

    # 只分析第一個 Repo，避免 Gemini 免費額度爆掉
    repo = repos[0]

    analysis = analyze_repo(
        repo["full_name"],
        repo.get("description", "")
    )

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI 商機雷達 V1</title>
    </head>

    <body>

        <h1>AI 商機雷達 V1</h1>

        <hr>

        <h2>{repo['full_name']}</h2>

        <p>
            ⭐ {repo['stargazers_count']} Stars
        </p>

        <p>
            {repo.get('description', '無描述')}
        </p>

        <hr>

        <pre>{analysis}</pre>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
