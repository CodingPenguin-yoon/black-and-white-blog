# 1단계: 마크다운 → 정적 HTML 빌드
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY build.py .
COPY posts ./posts
COPY static ./static
RUN python build.py

# 2단계: 빌드 결과물(dist/)만 nginx로 서빙
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
