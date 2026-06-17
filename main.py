from flask import Flask
from collectors.github_collector import get_trending

app = Flask(__name__)

@app.route("/")
def home():

    data = get_trending()

    result = []

    for repo in data["items"][:10]:
        result.append(
            f"{repo['full_name']} ⭐{repo['stargazers_count']}"
        )

    return "<br>".join(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
