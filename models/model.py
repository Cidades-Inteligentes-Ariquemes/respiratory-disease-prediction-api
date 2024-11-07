from ultralytics import YOLO

def load_model():
    model = YOLO('models/best.pt')
    return model

def load_model_breast_cancer():
    model = YOLO('models/best_breast_cancer.pt')
    return model
