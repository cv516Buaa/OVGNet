
<p align="center">
  <h1 align="center">OVGNet: An Unified Visual-Linguistic Framework for Open-Vocabulary Robotic Grasping</h1>
  <p align="center">


   <br />
    <strong>Meng Li</strong></a>
    ·
    <strong>Qi Zhao</strong></a>
    ·
    <a href="https://cv-shuchanglyu.github.io/EnHome.html"><strong>Shuchang Lyu</strong></a>
    ·
    <strong>Chunlei Wang</strong></a>    
    ·
    <strong>Yujing Ma</strong></a>
    ·
    <a href="https://sites.google.com/view/guangliangcheng"><strong>Guangliang Cheng</strong></a>
    ·
    <strong>Chenguang Yang</strong></a>
    <br />
<p align="center">

    
  </p>





## Highlight!!!!
This repo is the implementation of "OVGNet: An Unified Visual-Linguistic Framework for Open-Vocabulary Robotic Grasping". we refer to [Vision-Language-Grasping](https://github.com/xukechun/Vision-Language-Grasping), [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO), [VL-Grasp](https://github.com/luyh20/VL-Grasp). Many thanks to these excellent repos.



## Demo Setting
* **Novel** indicates the **unseen** objects in training.
* **Base** denotes the **seen** objects in training.
* Battery and power drill are novel classes, which belong to hard task.
* Apple and pear are base classes, which belong to simple task.

      





## Demo Video


[Demo](https://github.com/cv516Buaa/OVGNet/assets/94512783/6a4a1f64-6c7f-4012-8774-60babf933290)


## Dataset
* [OVGrasping](https://pan.baidu.com/s/113wBIJ-hWnSJNkWlngPqAg?pwd=8667) follows GroundingDINO data format.
* The OVGrapsing dataset comprises 117 categories and 63,385 instances.
* Instances are sourced from three distinct origins: RoboRefIt, GraspNet, simulated environment.
* The dataset is divided into two categories: the base category consists 51,857 instances, and the novel category comprises 11,528 instances. 

## Installation
* Ubantu==18.04
* Python==3.9 
* Torch==1.11, Torchvision==0.12.0
* CUDA==11.3
* checkpoint==[OVGANet](https://pan.baidu.com/s/13j4XBza1LNzsh-5RSfdFiQ?pwd=f3md)
* assets==[assets](https://pan.baidu.com/s/1vUestnCMZKZU5Kb2lC1LMA?pwd=uov1)

**please add the assets into OVGNet folder**
<br />
**please ensure the CUDA version is 11.3**
```
conda create -n OVGNet python=3.9
conda activate OVGNet
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
```


```
cd /OVGNet/
pip install -r requirments.txt
```

```
cd graspnet/graspnet/pointnet2
python setup.py install
cd graspnet/graspnet/knn
python setup.py install
cd groundingdino
pip install -e .
```

## Run
```
cd /OVGNet/
python test.py --testing_case_dir ./test_cases/simple/apple --pretrain ./checkpoint/OVGANet
```

## Test on OVGrasping
```
cd /OVGNet/test_vg/
python test_vg.py --c ./config/cfg_odvg.py --datasets ./config/datasets_vg_example.json --pretrain_model_path  OVGNet/checkpoint/OVGANet
```

## Cite
```
@InProceedings{Li_2024_IROS,
    author = {Li Meng and Zhao Qi and Lyu Shuchang and Wang Chunlei and Ma Yujing and Cheng Guangliang and Yang Chenguang},
    title = {OVGNet: A Unified Visual-Linguistic Framework for Open-Vocabulary Robotic Grasping},
    year = {2024},
    eprint = {2407.13175},
    archivePrefix = {arXiv},
    primaryClass = {cs.RO},
    url = {https://arxiv.org/abs/2407.13175}, 
}
