from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
import re

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BRAND = "Black &amp; White"
MARKDOWN = MarkdownIt("commonmark", {"html": False})


@dataclass
class Post:
    published: date
    slug: str
    title: str
    body: str


def read_post(path):
    name = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)", path.stem)
    heading, _, body = path.read_text(encoding="utf-8").partition("\n")
    if not name or not heading.startswith("# ") or not heading[2:].strip():
        raise ValueError(f"{path.name} — 날짜-슬러그.md 형식의 파일명과 첫 줄의 # 제목이 필요합니다.")
    return Post(date.fromisoformat(name[1]), name[2], escape(heading[2:].strip()), MARKDOWN.render(body))


def page(title, content, prefix, heading_font):
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#000000">
  <title>{title}</title>
  <link rel="preload" href="{prefix}fonts/{heading_font}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
  <main>
    {content}
  </main>
</body>
</html>
"""


def build():
    posts = sorted(
        (read_post(path) for path in (ROOT / "posts").glob("*.md")),
        key=lambda post: (post.published, post.slug),
        reverse=True,
    )
    slugs = {post.slug for post in posts}
    if len(slugs) != len(posts):
        raise ValueError("각 글의 슬러그는 고유해야 합니다.")

    links = "\n        ".join(
        f'<li><a href="./posts/{post.slug}/"><span aria-hidden="true">$</span> {post.title}</a></li>'
        for post in posts
    )
    home = f"""<h1 class="signature" lang="en">{BRAND}</h1>
    <nav class="entries" aria-label="글 목록">
      <ul>
        {links}
      </ul>
    </nav>"""
    (DIST / "index.html").write_text(page(BRAND, home, "./", "mr-dafoe-latin.woff2"), encoding="utf-8")

    for post in posts:
        article = f"""<nav aria-label="블로그">
      <a class="home-link" href="../../" aria-label="cd .. · 글 목록으로 돌아가기"><span aria-hidden="true">$</span> cd ..</a>
    </nav>
    <article>
      <h1>{post.title}</h1>
      <div class="prose">
        {post.body.strip()}
      </div>
    </article>"""
        output = DIST / "posts" / post.slug / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        html = page(f"{post.title} · {BRAND}", article, "../../", "chakra-petch-semibold-latin.woff2")
        output.write_text(html, encoding="utf-8")

    for old in (DIST / "posts").glob("*/index.html"):
        if old.parent.name not in slugs:
            old.unlink()


if __name__ == "__main__":
    build()
