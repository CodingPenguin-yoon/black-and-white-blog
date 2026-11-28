# Black & White

`posts/2026-11-19-first.md`처럼 `posts/YYYY-MM-DD-slug.md` 파일을 만든다. 첫 줄에는 `# 제목`을, 빈 줄 아래에는 마크다운 본문을 쓴다. 파일명의 날짜는 글 순서를, 슬러그는 글 주소를 정한다.

처음 한 번 `python3 -m pip install -r requirements.txt`로 의존성을 준비한다. `python3 build.py`를 실행하면 `dist/`를 비우고 `static/`의 스타일·폰트를 복사한 뒤 목록과 본문을 생성한다. `python3 -m http.server --directory dist`로 배포 전에 읽어볼 수 있다.

## 구조

- `posts/` — 글 원본 (마크다운)
- `static/` — 그대로 복사되는 정적 파일 (CSS, 폰트)
- `build.py` — 정적 사이트 생성기
- `dist/` — 빌드 결과물. Git에 올리지 않으며 배포 시 CI가 만든다.

## 배포

`Dockerfile`이 빌드와 서빙을 모두 맡는다. 1단계에서 Python으로 `dist/`를 만들고, 2단계에서 nginx가 그 결과물만 80번 포트로 서빙한다.

```sh
docker build -t black-and-white .
docker run --rm -p 8080:80 black-and-white   # http://localhost:8080
```

배포 플랫폼에서는 이미지를 빌드한 뒤 컨테이너 포트 `80`을 연결하면 된다. nginx 설정은 `nginx.conf`에 있다.
