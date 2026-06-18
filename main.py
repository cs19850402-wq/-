from flask import Flask
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_trending():
    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"

    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json"
        }
    )

    if response.status_code == 200:
        return response.json()["items"][:10]

    return []


def analyze_repo(repo_name, description):

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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

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
        r = requests.post(url, json=payload)

        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except:
        return "Gemini分析失敗"


@app.route("/")
def home():

    repos = get_trending()

    html = """
    <h1>AI 商機雷達 V1</h1>
    <hr>
    """

    for repo in repos[:5]:

        analysis = analyze_repo(
            repo["full_name"],
            repo.get("description", "")
        )

        html += f"""
        <h2>{repo['full_name']}</h2>

        ⭐ {repo['stargazers_count']} Stars

        <br><br>

        {repo.get('description','')}

        <br><br>

        <pre>{analysis}</pre>

        <hr>
        """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
