import os
import jsonlines
import random
import json
folder_path = '/media/lm/Elements/新标的数据/novel/label/'
sorted_list = sorted(os.listdir(folder_path))
new_data = []
language_data = []
count = 0
test_list = ['give me the', 'hand me the', 'grab the', 'grasp the', 'bring me the', 'pick up the', 'find the', 'I need the',
             'fetch me the', 'I want use the', 'I need use the', 'I want grasp the', 'can you find the'
             ]
for f in sorted_list:
    path = folder_path + f
    file = os.listdir(path)
    file.sort()
    d = f[3:]
    d = d[:-6]
    b = f[:2]
    for a in file:
        path1 = path + "/" + a
        name = a[:7]
        c = random.choice(test_list)
        c = c + ' ' + d
        with open(path1, 'r') as ff:
            lines = ff.readlines()
            for line in lines:
                line = line.strip()
                elements = line.split()
                x_center, y_center, width, height = map(float, elements[1:5])
                x1 = (x_center - (width / 2)) * 640
                y1 = (y_center - (height / 2)) * 480
                x2 = (x_center + (width / 2)) * 640
                y2 = (y_center + (height / 2)) * 480
                bbox = [round(x1), round(y1), round(x2), round(y2)]
                annotation = {'filename': "{}.png".format(name),
                              'class': '{}'.format(b),
                              'text': '{}'.format(c),
                              'bbox': bbox
                              }
                new_data.append(annotation)
                count += 1
new_data = list(filter(None, new_data))
with jsonlines.open('/media/lm/Elements/新标的数据/novel/base.jsonl', mode="w") as fwriter:
    fwriter.write_all(new_data)
# with open('/home/lm/Desktop/testA/VGtest/seen/multi_language.txt', 'r') as f:
#     lines = [line.rstrip('\n') for line in f]
#     for line in lines:
#         language_data.append(line)
# for filename in sorted_list:
#     name = filename[:7]
#     with open(folder_path+'/'+filename, 'r') as file:
#         lines = file.readlines()
#         for line in lines:
#             line = line.strip()
#             elements = line.split()
#             x_center, y_center, width, height = map(float, elements[1:5])
#             x1 = (x_center - (width / 2))*640
#             y1 = (y_center - (height / 2))*480
#             x2 = (x_center + (width / 2))*640
#             y2 = (y_center + (height / 2))*480
#             bbox = [round(x1), round(y1), round(x2), round(y2)]
#             annotation = {'filename': "{}.jpg".format(name),
#                           'height': 480,
#                           'width': 640,
#                           'grounding': {"caption": "{}".format(language_data[count]),
#                           "regions": [{"bbox": bbox, "phrase": "{}".format(language_data[count])}]}}
#             count += 1
#             new_data.append(annotation)


# dict_list5 = []
# dict_list4 = []
#
# with open('/home/lm/Desktop/testA/VGtest/seen/single_test.jsonl', 'r') as file:
#     for line in file:
#         try:
#             # 尝试将行解析为JSON
#             dict_list5.append(json.loads(line))
#         except json.JSONDecodeError as e:
#             # 打印错误信息，并继续处理下一行
#             print(f"JSON 解析错误: {e.msg} 在行 {e.lineno}")
#             print(line)
#             continue
#         except Exception as e:
#             # 捕获任何其他类型的异常
#             print(f"在处理行时发生未知错误: {e}")
# with open('/media/lm/T7 Shield/1_biaozhu/grasp_train/222train4000.jsonl', 'r') as file:
#     for line in file:
#         try:
#             # 尝试将行解析为JSON
#             dict_list4.append(json.loads(line))
#         except json.JSONDecodeError as e:
#             # 打印错误信息，并继续处理下一行
#             print(f"JSON 解析错误: {e.msg} 在行 {e.lineno}")
#             print(line)
#             continue
#         except Exception as e:
#             # 捕获任何其他类型的异常
#             print(f"在处理行时发生未知错误: {e}")
# a = 1