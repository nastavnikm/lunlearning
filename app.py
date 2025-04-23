from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_b92_news():
    url = "https://www.b92.net/najnovije-vesti"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    news_items = soup.find_all("div", class_="news-item-data")
    vesti = []
    for item in news_items:
        title_tag = item.find("h2", class_="news-item-title").find("a")
        title = title_tag.find("span").text.strip() if title_tag else None

        pre_vreme_number = item.find("span", class_="before-time-number")
        pre_vreme_text = item.find("span", class_="before-time-text")
        vreme = ""
        if pre_vreme_number and pre_vreme_text:
            vreme = f"{pre_vreme_number.text.strip()} {pre_vreme_text.text.strip()}"

        if title and vreme:
            text = f"***B92*** [{vreme}] {title}"
            vesti.append(text)

    return vesti


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_news", methods=["POST"])
def get_news():
    data = request.json
    sites = data.get("sites", [])
    sve_vesti = []

    if "B92" in sites:
        sve_vesti.extend(get_b92_news())

    # Dodaj RTS, N1 i druge sajtove ako je potrebno
    # if "RTS" in sites:
    #     sve_vesti.extend(get_rts_news())

    return jsonify(sve_vesti)


if __name__ == "__main__":
    app.run(debug=True)
