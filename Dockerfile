FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder

LABEL maintainer="Przemek Zbiciak"

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM --platform=$TARGETPLATFORM python:3.12-alpine

LABEL maintainer="Przemek Zbiciak"

WORKDIR /app

COPY --from=builder /install /usr/local/
COPY app.py .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import socket; s=socket.create_connection(('localhost', 5000), timeout=2).close()"

EXPOSE 5000

CMD ["python", "app.py"]
