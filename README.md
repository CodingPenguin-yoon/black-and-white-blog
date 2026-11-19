# Black & White

`posts/2026-11-19-first.md`처럼 `posts/YYYY-MM-DD-slug.md` 파일을 만든다. 첫 줄에는 `# 제목`을, 빈 줄 아래에는 마크다운 본문을 쓴다. 파일명의 날짜는 글 순서를, 슬러그는 글 주소를 정한다.

처음 한 번 `python3 -m pip install -r requirements.txt`로 의존성을 준비한다. `python3 build.py`를 실행하면 `dist/`에 목록과 본문이 생성된다. `python3 -m http.server --directory dist`로 배포 전에 읽어볼 수 있다.
