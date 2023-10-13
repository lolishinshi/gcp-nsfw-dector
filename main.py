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

    def predict(self, image: Image.Image):
        image = self.process_image(image)
        preds = self.model.run(None, {'input': [image]})[0][0]
        probs = {}
        for i, pred in enumerate(preds):
            probs[self.categories[i]] = round(float(pred), 4)
        return probs

detector = NSFWDector('model/mobilenet_v2_140_224.onnx')


@functions_framework.http
def detect(request: Request):
    if request.method != 'POST':
        return 'Method not allowed', 405

    files = request.files.getlist('images')
    if not files:
        return 'No images found', 400
    
    return [
        detector.predict(Image.open(f))
        for f in files
    ]
