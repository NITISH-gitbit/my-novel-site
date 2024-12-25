import os
from flask import Flask, render_template
import re

app = Flask(__name__)

CHAPTERS_DIR = "chapters"

def load_chapters():
    chapters = []
    # List all files in the chapters directory
    for file_name in sorted(os.listdir(CHAPTERS_DIR), key=lambda x: int(re.search(r'(\d+)', x).group(1))):
        if file_name.endswith(".txt"):
            chapter_title = os.path.splitext(file_name)[0].replace('_', ' ').title()
            chapters.append({"title": chapter_title, "file": file_name})
    return chapters

@app.route("/")
def index():
    chapters = load_chapters()
    return render_template("index.html", chapters=chapters)

@app.route("/chapter/<file_name>")
def chapter(file_name):
    file_path = os.path.join(CHAPTERS_DIR, file_name)
    if not os.path.exists(file_path):
        return "Chapter not found", 404
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    title = os.path.splitext(file_name)[0].replace('_', ' ').title()
    return render_template("chapter.html", title=title, content=content)

if __name__ == "__main__":
    app.run(debug=True)
