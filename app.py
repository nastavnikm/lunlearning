from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    messages = []
    folder_path = "messages"  # Folder gde će biti tekstualne poruke
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            filepath = os.path.join(folder_path, filename)
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    messages.append(f.read())
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
