FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --user -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

ENV PATH="/root/.local/bin:$PATH"

EXPOSE 5000

CMD ["python", "app.py"]