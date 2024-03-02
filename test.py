import argparse
import numpy as np
import random
import torch
import os

import utils
from constants import WORKSPACE_LIMITS
from environment_sim import Environment
from logger import Logger
from grasp_detetor import Graspnet
from demo.inference_on_a_image import get_grounding_output
from demo.inference_on_a_image import load_model
from demo.inference_on_a_image import load_image
from PIL import Image
from utils import switch_one_grasp
import pybullet as pb

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--device', action='store', type=str, default='cuda')
    parser.add_argument('--seed', type=int, default=6666, metavar='N',
                    help='random seed (default: 1234)')
    parser.add_argument('--testing_case_dir', action='store', type=str, default='test_cases/simple/apple')
    parser.add_argument('--pretrain', action='store', type=str, default='checkpoint/OVGAnet')
    parser.add_argument('--testing_case', action='store', type=str, default=None)
    parser.add_argument('--num_episode', action='store', type=int, default=1)
    parser.add_argument('--max_episode_step', type=int, default=3)

    #Groundinghdino
    parser.add_argument("--box_threshold", type=float, default=0.1, help="box threshold")
    parser.add_argument("--text_threshold", type=float, default=0.1, help="text threshold")
    parser.add_argument("--token_spans", type=str, default=None, help=
                        "The positions of start and end positions of phrases of interest. ")
    parser.add_argument("--cpu-only", action="store_true", help="running on cpu only!", default=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()
    
    # set device and seed
    args.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    num_episode = args.num_episode

    env = Environment(gui=True)
    env.seed(args.seed)
    logger = Logger(case_dir=args.testing_case_dir)
    graspnet = Graspnet()
    config_file = './groundingdino/config/GroundingDINO_SwinT_OGC.py'
    checkpoint_path = args.pretrain
    model = load_model(config_file, checkpoint_path, cpu_only=args.cpu_only)
    box_threshold = args.box_threshold
    text_threshold = args.text_threshold

    if os.path.exists(args.testing_case_dir):
        filelist = os.listdir(args.testing_case_dir)
        filelist.sort()
    if args.testing_case != None:
        filelist = [args.testing_case]
    case = 0
    iteration = 0
    count = 0
    total_count = len(filelist)
    for f in filelist:
        f = os.path.join(args.testing_case_dir, f)

        logger.episode_reward_logs = []
        logger.episode_step_logs = []
        logger.episode_success_logs = []
        for episode in range(num_episode):
            episode_reward = 0
            episode_steps = 0
            done = False
            reset = False

            while not reset:
                env.reset()
                reset, lang_goal = env.add_object_push_from_file(f)
                print(f"\033[032m Reset environment of episode {episode}, language goal {lang_goal}\033[0m")

            while not done:
                # check if one of the target objects is in the workspace:
                out_of_workspace = []
                for obj_id in env.target_obj_ids:
                    pos, _, _ = env.obj_info(obj_id)
                    if pos[0] < WORKSPACE_LIMITS[0][0] or pos[0] > WORKSPACE_LIMITS[0][1] \
                        or pos[1] < WORKSPACE_LIMITS[1][0] or pos[1] > WORKSPACE_LIMITS[1][1]:
                        out_of_workspace.append(obj_id)
                if len(out_of_workspace) == len(env.target_obj_ids):
                    print("\033[031m Target objects are not in the scene!\033[0m")
                    break


                color1, depth, segm = env.render_camera(env.oracle_cams1[0])

                color = Image.fromarray(color1)

                img_pil, color_image = load_image(color)

                pb.addUserDebugText(text=lang_goal, textPosition=[0.8, -0.2, 0], textColorRGB=[0, 0, 1],
                                    textSize=2)
                boxes_filt, pred_phrases = get_grounding_output(
                    model, color_image, lang_goal, box_threshold, text_threshold, cpu_only=args.cpu_only,
                    token_spans=None
                )

                pcd = utils.get_fuse_pointcloud(env, boxes_filt, color1, depth)

                with torch.no_grad():
                    grasp_pose_set, _, _, = graspnet.grasp_detection(pcd, env.get_true_object_poses())
                print("Number of grasping poses", len(grasp_pose_set))
                if len(grasp_pose_set) == 0:
                    break
                if len(grasp_pose_set) == 1:
                    action_idx = 0
                else:
                    action_idx = switch_one_grasp(boxes_filt, grasp_pose_set)
                action = grasp_pose_set[action_idx]
                done, counts = env.step(action)
                if counts:
                    count += 1
                iteration += 1
                episode_steps += 1
                print("\033[034m Episode: {}, step: {}, grasp_success: {}\033[0m".format(episode, episode_steps, count/total_count))

                if episode_steps == args.max_episode_step:
                    break
