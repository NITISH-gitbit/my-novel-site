import os
import re
from flask import Flask, render_template, abort

app = Flask(__name__)

CHAPTERS_DIR = "chapters"

def load_chapters():
    """
    Load all chapter files from the chapters directory and return
    a sorted list of dictionaries containing title and file name.
    """
    chapters = []
    for file_name in sorted(
        os.listdir(CHAPTERS_DIR),
        key=lambda x: int(re.search(r'(\d+)', x).group(1))
    ):
        if file_name.endswith(".txt"):
            chapter_title = os.path.splitext(file_name)[0].replace('_', ' ').title()
            chapters.append({"title": chapter_title, "file": file_name})
    return chapters

@app.route("/")
def index():
    """
    Display the homepage with the list of chapters.
    """
    chapters = load_chapters()
    return render_template("index.html", chapters=chapters)

@app.route("/chapter/<file_name>")
def chapter(file_name):
    """
    Display a specific chapter with navigation and proper formatting.
    """
    chapters = load_chapters()
    file_path = os.path.join(CHAPTERS_DIR, file_name)
    
    if not os.path.exists(file_path):
        abort(404)  # Return a 404 error if chapter doesn't exist

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split content into paragraphs
    paragraphs = content.strip().split("\n\n")
    
    # Get the current chapter index
    current_index = next((i for i, ch in enumerate(chapters) if ch["file"] == file_name), None)
    if current_index is None:
        abort(404)
    
    # Determine next and previous chapters
    next_chapter = chapters[current_index + 1] if current_index + 1 < len(chapters) else None
    previous_chapter = chapters[current_index - 1] if current_index > 0 else None
    
    return render_template(
        "chapter.html",
        title=chapters[current_index]["title"],
        paragraphs=paragraphs,
        next_chapter=next_chapter,
        previous_chapter=previous_chapter,
        chapters=chapters
    )

if __name__ == "__main__":
    app.run(debug=True)
