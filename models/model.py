from ultralytics import YOLO

def load_model():
    model = YOLO('models/best.pt')
    return model
