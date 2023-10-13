import functions_framework
import onnxruntime
import numpy as np
from PIL import Image
from werkzeug import Request


class NSFWDector:
    def __init__(self, model_path: str, dim: int = 224):
        self.model = onnxruntime.InferenceSession(model_path)
        self.categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']
        self.dim = dim

    def process_image(self, image: Image.Image):
        image = image.convert('RGB').resize((self.dim, self.dim))
        image = np.asarray(image, dtype=np.float32) / 255
        return image

    def predict(self, images: list[Image.Image]):
        images = [self.process_image(img) for img in images]

        model_preds = self.model.run(None, {'input': images})

        probs = []
        for single_preds in model_preds[0]:
            single_probs = {}
            for i, pred in enumerate(single_preds):
                single_probs[self.categories[i]] = round(float(pred), 4)
            probs.append(single_probs)

        return probs

detector = NSFWDector('model/mobilenet_v2_140_224.onnx')


@functions_framework.http
def detect(request: Request):
    if request.method != 'POST':
        return 'Method not allowed', 405

    files = request.files.getlist('images')
    if not files:
        return 'No images found', 400

    images = [Image.open(f) for f in files]

    preds = detector.predict(images)
    return preds

