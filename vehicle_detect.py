# YOLOv5 by Ultralytics, GPL-3.0 license
# Open Source by Maryam Boneh, Vehicle-Detection from github (link)
# Edited by Team CP0
import sys
from pathlib import Path

import cv2
import numpy as np
import torch

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, is_ascii, non_max_suppression, \
    scale_coords, xyxy2xywh, strip_optimizer, save_one_box
from utils.plots import Annotator, colors

from util import MODEL_DIR, DETECTED_IMAGE_DIR, CAPTURED_IMAGE_DIR
from util import deleteFiles


weights=MODEL_DIR+"pt/best.pt"
w = weights[0] if isinstance(weights, list) else weights
classify, suffix = False, Path(w).suffix.lower()
stride, names = 64, [f'class{i}' for i in range(1000)]


@torch.no_grad()
def vehicle_detection(name):

    global weights, stride

    source = CAPTURED_IMAGE_DIR + name
    imgsz=128  
    conf_thres=0.25 
    iou_thres=0.45  
    max_det=5  
    device='cpu' 
    classes=None  
    agnostic_nms=False  
    augment=False  
    visualize=False  
    update=False  

    save_dir = Path("images") / "detected" 
    xy_list = []

    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    names = model.module.names if hasattr(model, 'module') else model.names 

    imgsz = check_img_size(imgsz, s=stride)
    ascii = is_ascii(names)

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=True)
    bs = 1 

    vid_path, vid_writer = [None] * bs, [None] * bs


    for path, img, im0s, vid_cap in dataset:

        img = torch.from_numpy(img).to(device)
        img = img.float()

        img = img / 255.0 


        if len(img.shape) == 3:
            img = img[None]
            
    
        pred = model(img, augment=augment, visualize=visualize)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)


        for i, det in enumerate(pred):  # detections per image

            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
            p = Path(p)
            s += '%gx%g ' % img.shape[2:]

            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

            imc = im0.copy() 

            annotator = Annotator(im0, line_width=0, pil=not ascii)


            if len(det):

                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += f"{n} {names[int(c)]}{' ' * (n > 1)}, "

                count = 1
                for *xyxy, conf, cls in reversed(det):

                    c = int(cls)

                    label = None
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    
                    xy_list.append([int(cls.item())]+[int(coord.item()) for coord in xyxy])
                    
                    # count for naming image file, actually save_one_box names automatically, but it won't name "1"
                    save_one_box(xyxy, imc, file=save_dir / f'{p.stem}{count}.jpg', BGR=True)
                    count += 1

        im0 = annotator.result()

        # change to consolelog someday
        print(xy_list)
        print(s)

    if update:
        strip_optimizer(weights)

    return xy_list





