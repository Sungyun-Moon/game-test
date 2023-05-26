FROM python:3.9

WORKDIR /app

# ソースコードをコンテナ内の/appディレクトリにコピーする
COPY game.py .

# 必要なパッケージをインストールする
RUN pip install pygame

CMD ["python", "game.py"]
