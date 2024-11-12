from ultralytics import YOLO
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

def load_model():
    model = YOLO('models/best.pt')
    return model

def load_model_breast_cancer():
    model = YOLO('models/best_breast_cancer.pt')
    return model

def load_model_breast_cancer_with_fatRCNN(device):
    num_classes = 3  

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None)

    # Obtem o número de características de entrada
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # Substitui o preditor por um novo com o número de classes desejado
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    model.load_state_dict(torch.load('models/faster_rcnn_model.pth', map_location=device))

    model.to(device)
    model.eval()

    return model
