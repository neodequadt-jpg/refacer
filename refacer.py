import cv2
import numpy as np
import onnxruntime as rt
from insightface.app import FaceAnalysis
from insightface.model_zoo.inswapper import INSwapper

class Refacer:
    def __init__(self, force_cpu=False):
        self.providers = ["CPUExecutionProvider"] if force_cpu else rt.get_available_providers()
        self.sess_options = rt.SessionOptions()
        self.sess_options.intra_op_num_threads = 4
        self.sess_options.inter_op_num_threads = 4
        self.face_detector = FaceAnalysis(
            name="buffalo_l",
            providers=self.providers
        )
        self.face_detector.prepare(ctx_id=0, det_size=(640, 640))
        self.face_swapper = None
        self.replacement_faces = []

    def _ensure_image(self, img):
        if isinstance(img, str):
            loaded = cv2.imread(img)
            if loaded is None:
                raise ValueError(f"Failed to load image from path: {img}")
            return loaded
        return img

    def prepare_faces(self, faces):
        self.replacement_faces = []
        for face in faces:
            origin = self._ensure_image(face["origin"])
            dest = self._ensure_image(face["destination"])
            faces1 = self.face_detector.get(origin)
            if len(faces1) == 0:
                raise ValueError("No face detected in origin image")
            faces2 = self.face_detector.get(dest)
            if len(faces2) == 0:
                raise ValueError("No face detected in destination image")
            # Сохраняем объекты лиц, а не только keypoints
            self.replacement_faces.append((faces1[0], faces2[0]))

    def swap_frame(self, frame, blend_strength=1.0):
        if self.face_swapper is None:
            raise RuntimeError("Face swapper not initialized")
        if not self.replacement_faces:
            raise RuntimeError("No replacement faces prepared")
        source_face, target_face = self.replacement_faces[0]
        swapped = self.face_swapper.get(
            frame,
            source_face,
            paste_back=True
        )
        return swapped
