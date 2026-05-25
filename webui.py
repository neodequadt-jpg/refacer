import gradio as gr
import cv2
import uuid
import os
import numpy as np
from tqdm import tqdm
from refacer import Refacer
import onnxruntime as rt
from insightface.model_zoo.inswapper import INSwapper

def load_swapper(model_path, ref):
    sess = rt.InferenceSession(model_path, ref.sess_options, providers=ref.providers)
    return INSwapper(model_path, sess)

def run_swap(origin_img, dest_img, model_path, blend_strength, progress=gr.Progress()):
    if origin_img is None or dest_img is None:
        return None
    ref = Refacer(force_cpu=False)
    ref.face_swapper = load_swapper(model_path, ref)
    faces = [{
        "origin": origin_img,
        "destination": dest_img,
        "threshold": 0.5
    }]
    ref.prepare_faces(faces)
    source_face, target_face = ref.replacement_faces[0]
    result = ref.face_swapper.get(
        dest_img,
        target_face,
        source_face,
        paste_back=True
    )
    out_path = f"/tmp/out_{uuid.uuid4().hex}.png"
    cv2.imwrite(out_path, result)
    return out_path

def run_video_swap(origin_img, video_file, model_path, blend_strength, progress=gr.Progress()):
    if origin_img is None or video_file is None:
        return None
    ref = Refacer(force_cpu=False)
    ref.face_swapper = load_swapper(model_path, ref)
    faces = [{
        "origin": origin_img,
        "destination": origin_img,
        "threshold": 0.5
    }]
    ref.prepare_faces(faces)
    source_face, _ = ref.replacement_faces[0]
    
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out_path = f"/tmp/out_{uuid.uuid4().hex}.mp4"
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    
    for _ in progress.tqdm(range(total), desc="Обработка видео"):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Детектим лицо в текущем кадре
        target_faces = ref.face_detector.get(frame)
        if len(target_faces) > 0:
            target_face = target_faces[0]
            try:
                swapped = ref.face_swapper.get(
                    frame,
                    target_face,
                    source_face,
                    paste_back=True
                )
                writer.write(swapped)
            except Exception as e:
                # Если ошибка при свопе, пишем оригинальный кадр
                print(f"Swap error: {e}, writing original frame")
                writer.write(frame)
        else:
            # Если лица не найдено, пишем оригинальный кадр
            writer.write(frame)
    
    cap.release()
    writer.release()
    return out_path

with gr.Blocks() as demo:
    gr.Markdown("# 🔥 Refacer WebUI (Docker‑Optimized Edition)")
    model_path = gr.Textbox(
        value="/app/models/inswapper_128.onnx",
        label="Путь к модели INSwapper"
    )
    blend_strength = gr.Slider(
        minimum=0.0,
        maximum=1.0,
        value=1.0,
        step=0.01,
        label="Blend Strength"
    )
    gr.Markdown("## 🖼️ FaceSwap для фото")
    with gr.Row():
        origin = gr.Image(label="Лицо‑источник")
        dest = gr.Image(label="Куда вставить лицо")
    out = gr.Image(label="Результат")
    btn = gr.Button("Swap Photo")
    btn.click(
        run_swap,
        inputs=[origin, dest, model_path, blend_strength],
        outputs=[out]
    )
    gr.Markdown("## 🎬 FaceSwap для видео")
    with gr.Row():
        origin_video = gr.Image(label="Лицо‑источник (фото)")
        video_input = gr.Video(label="Видео для обработки")
    video_out = gr.Video(label="Результат")
    btn_video = gr.Button("Swap Video")
    btn_video.click(
        run_video_swap,
        inputs=[origin_video, video_input, model_path, blend_strength],
        outputs=[video_out]
    )

demo.queue().launch(server_name="0.0.0.0", server_port=7860)
