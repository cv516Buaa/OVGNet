import numpy as np

def lm_select_box(outputs, captions, true_boxes, threshold, index1):
    logits = outputs["pred_logits"].sigmoid()  # (nq, 256)
    boxes = outputs["pred_boxes"]  # (nq, 4)

    # filter output
    logits_filt = logits.cpu().clone()
    boxes_filt = boxes.cpu().clone()
    filt_mask = logits_filt.max(dim=2)[0]
    filt_mask = filt_mask.numpy()
    filt_max = np.argmax(filt_mask, axis=1)
    out_boxs = []
    for index, value in enumerate(filt_max):
        xyxy = boxes_filt[index][value].numpy()
        # xyxy = [xyxy[0] - xyxy[2] / 2, xyxy[1] - xyxy[3] / 2, xyxy[0] + xyxy[2] / 2, xyxy[1] + xyxy[3] / 2]
        out_boxs.append(xyxy)
    if len(index1) == 0:
        out_boxs = out_boxs
    elif len(index1) > 1:
        out_boxs = [j for i, j in enumerate(out_boxs) if i not in index1]
    elif len(index1) == 1:
        del out_boxs[index1[0]]

    gt = []
        # true_boxes = true_boxes[0]
    for i, ii in enumerate(true_boxes):
        gt1 = true_boxes[i].numpy().squeeze()
        gt.append(gt1)
    ious = np.diag(compute_multiple_ious(out_boxs, gt))
    tp = 0
    for iii in ious:
        if iii > threshold:
            tp +=1
        else:
            continue
    return tp



def compute_iou(box1, box2):
    xA = max(box1[0] - box1[2] / 2, box2[0] - box2[2] / 2)
    yA = max(box1[1] - box1[3] / 2, box2[1] - box2[3] / 2)
    xB = min(box1[0] + box1[2] / 2, box2[0] + box2[2] / 2)
    yB = min(box1[1] + box1[3] / 2, box2[1] + box2[3] / 2)

    interArea = max(0, xB - xA) * max(0, yB - yA)

    box1Area = box1[2] * box1[3]
    box2Area = box2[2] * box2[3]

    iou = interArea / (box1Area + box2Area - interArea)

    return iou

def compute_multiple_ious(pred_boxes, true_boxes):
    ious = np.zeros((len(pred_boxes), len(true_boxes)))

    for i, pred_box in enumerate(pred_boxes):
        for j, true_box in enumerate(true_boxes):
            ious[i, j] = compute_iou(pred_box, true_box)

    return ious

















