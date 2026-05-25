#!/bin/bash

URL="https://huggingface.co/facefusion/models-3.3.0/resolve/main/face_dat_x4.onnx"
OUT="face_dat_x4.onnx"
aria2c \
  --no-conf \
  --no-proxy \
  --allow-overwrite=true \
  --continue=true \
  --max-connection-per-server=32 \
  --split=32 \
  --min-split-size=1M \
  --max-tries=0 \
  --retry-wait=2 \
  --timeout=60 \
  --connect-timeout=60 \
  --enable-http-pipelining=true \
  --enable-http-keep-alive=true \
  --file-allocation=none \
  --auto-file-renaming=false \
  --summary-interval=5 \
  -o "$OUT" \
  "$URL"

echo "[+] Download finished:"
ls -lh "$OUT"
