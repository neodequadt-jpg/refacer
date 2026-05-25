FROM python:3.10-slim

RUN apt-get update && apt-get install -y nano \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip setuptools wheel

RUN pip install \
    onnxruntime==1.17.0 \
    insightface==0.7.3 \
    opencv-python-headless \
    numpy \
    pillow \
    tqdm \
    scipy \
    ffmpeg-python \
    psutil \
    requests \
    scikit-image \
    gradio==3.50.2 \
    fastapi==0.103.0 \
    starlette==0.27.0 \
    pydantic==1.10.15 \
    jinja2==3.1.2 \
    markdown-it-py==2.2.0

RUN mkdir -p /app/models && \
    curl -L -o /app/models/inswapper_128.onnx \
    https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx

EXPOSE 7860
CMD ["python3", "webui.py"]

