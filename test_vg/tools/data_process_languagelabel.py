import json
import os
import jsonlines
import cv2
# with open('/home/lm/Desktop/train.jsonl', 'r') as f:
#     for line in f:
#         new_line = []
#         new_line.append(json.load(line))
#         print(new_line)
#         imge_plr = new_line["filename"]
#         a = new_line["grounding"]
#         b =1
import json

data = []
with open('/home/lm/Desktop/train.jsonl', 'r') as file:
    for line in file:
        # json.loads 将 JSON 字符串转换为 Python 对象
        data.append(json.loads(line))
        print(line)
print(len(data))
# H, W = tgt["size"]
# boxes = tgt["boxes"]
# labels = tgt["labels"]
# assert len(boxes) == len(labels), "boxes and labels must have same length"
#
# draw = ImageDraw.Draw(image_pil)
# mask = Image.new("L", image_pil.size, 0)
# mask_draw = ImageDraw.Draw(mask)
#
# # draw boxes and masks
# for box, label in zip(boxes, labels):
#     # from 0..1 to 0..W, 0..H
#     box = box * torch.Tensor([W, H, W, H])
#     # from xywh to xyxy
#     box[:2] -= box[2:] / 2
#     box[2:] += box[:2]
#     # random color
#     color = tuple(np.random.randint(0, 255, size=3).tolist())
#     # draw
#     x0, y0, x1, y1 = box
#     x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
#
#     draw.rectangle([x0, y0, x1, y1], outline=color, width=6)
#     # draw.text((x0, y0), str(label), fill=color)
#
#     font = ImageFont.load_default()
#     if hasattr(font, "getbbox"):
#         bbox = draw.textbbox((x0, y0), str(label), font)
#     else:
#         w, h = draw.textsize(str(label), font)
#         bbox = (x0, y0, w + x0, y0 + h)
#     # bbox = draw.textbbox((x0, y0), str(label))
#     draw.rectangle(bbox, fill=color)
#     draw.text((x0, y0), str(label), fill="white")
#
#     mask_draw.rectangle([x0, y0, x1, y1], fill=255, width=6)