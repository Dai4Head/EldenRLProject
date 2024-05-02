import gym
import numpy as np
import cv2
import time

from gym import spaces
# 从直接键盘操作库中导入按键函数
from directkeys import (
    PressKey, ReleaseKey, W, A, S, D, V, LSHIFT, R, E, F, Q, J, K, L, ESC, DOWN, G,
    attack, attack2, attack3, attack4,
    go_forward, go_back, go_left, go_right,
    dodge, forward_dodge, back_dodge, left_dodge, right_dodge,
    jump, forward_jump, lock_vision, start_boss, pause_game, heal
)
from restart import restart  # 重启游戏并走到Boss处的函数
from Screen_Graber import capture_window  # 屏幕捕获函数
from HP_Finder import get_health_and_mana  # 血量和蓝量读取函数
from EldenReward import EldenReward  # 奖励计算类

# 动作函数映射
ACTION_FUNCTION_MAPPING = {
    'go_forward': go_forward,
    'go_back': go_back,
    'go_left': go_left,
    'go_right': go_right,
    'dodge': dodge,
    'forward_dodge': forward_dodge,
    'back_dodge': back_dodge,
    'left_dodge': left_dodge,
    'right_dodge': right_dodge,
    'attack': attack,
    'attack2': attack2,
    'attack3': attack3,
    'attack4': attack4,
    # 'jump': jump,
    # 'forward_jump': forward_jump,
    'heal': heal
}

DISCRETE_ACTIONS = {k: v for k, v in enumerate(ACTION_FUNCTION_MAPPING.keys())}
NUMBER_DISCRETE_ACTIONS = len(DISCRETE_ACTIONS)
NUM_ACTION_HISTORY = 10
# step_counter = 0 # 用于减少print次数的变量
currenttime = 0

class EldenEnv(gym.Env):
    # 游戏环境，遵循Gym接口

    def __init__(self, config):
        super(EldenEnv, self).__init__()
    
        # 先设置默认值
        self.model_width = config.get('model_width', 1622)  # 默认值1622
        self.model_height = config.get('model_height', 956)  # 默认值956
    
        self.action_space = spaces.Discrete(NUMBER_DISCRETE_ACTIONS)
        # 使用已设置的默认值来定义observation_space
        self.observation_space = spaces.Dict({
            'img': spaces.Box(low=0, high=255, shape=(self.model_height, self.model_width, 4), dtype=np.uint8),
            'prev_actions': spaces.Box(low=0, high=1, shape=(NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS), dtype=np.uint8),
            'state': spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32),
        })
        
        # 初始化 prev_actions 数组
        self.prev_actions = np.zeros((NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS), dtype=np.uint8)
        
        self.window_title = config.get('window_title', 'ELDEN RING™')
        self.rewardGen = EldenReward(config)  # 初始化奖励计算类
        # # 解决进房reset问题的一种尝试
        # self.rewardGen = EldenReward(config)
        # self.rewardGen.ignore_death_time = 0
        
        # self.last_reset_time # 记录reset时间

        self.training_round = 0
        self.action_count = 0
        self.round_rewards = []
        
        self.done = False
        # 打印动作映射以验证正确性
        print("Action mappings:")
        for k, v in DISCRETE_ACTIONS.items():
            print(f"Action {k}: {v}")
            

    def grab_screen_shot(self):
        return capture_window(self.window_title)

    def take_action(self, action):
        action_func_name = DISCRETE_ACTIONS[action]
        if action_func_name in ACTION_FUNCTION_MAPPING:
            # print(f"执行的动作是: {action_func_name}")
            ACTION_FUNCTION_MAPPING[action_func_name]()
    
    def calculate_health_and_mana(self):
        return get_health_and_mana(self.window_title)

    def step(self, action):
        if not hasattr(self, 'first_step'):
            self.first_step = True
        frame = self.grab_screen_shot()
        health, boss_health, mana = self.calculate_health_and_mana()
        total_reward, is_dead, is_boss_dead = self.rewardGen.update(frame, self.first_step)
        self.first_step = False
    
        observation = cv2.resize(frame, (self.model_width, self.model_height))
        info = {}
        self.done = is_dead or is_boss_dead

        # print(f"Executing action: {DISCRETE_ACTIONS[action]}")
        self.take_action(action)
        
        # prev_actions 更新
        prev_actions = np.zeros((NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS, 1), dtype=np.uint8)
        prev_actions = np.roll(prev_actions, shift=1, axis=0)
        prev_actions[0, action, 0] = 1  # 更新最新动作
    
        state = np.array([health, boss_health, mana])
    
        # FPS限制逻辑，确保每步间隔一定时间
        time.sleep(0.2)  # 保证每个动作之间至少有0.2秒的间隔
        
        self.action_count += 1
        self.round_rewards.append(total_reward)
        if self.done:
            print(f"End of Round {self.training_round}: Boss HP {self.rewardGen.boss_last_check}, Actions taken {self.action_count}, Total reward {sum(self.round_rewards)}")
            with open("training_log.txt", "a") as file:
                file.write(f"Round {self.training_round}: Boss HP {self.rewardGen.boss_last_check}, Actions {self.action_count}, Total reward {sum(self.round_rewards)}\n")
        
        new_prev_actions = np.roll(self.prev_actions, shift=1, axis=0)
        new_prev_actions[0] = np.zeros((NUMBER_DISCRETE_ACTIONS,))
        new_prev_actions[0, action] = 1  # 将当前动作设置在最前
        self.prev_actions = new_prev_actions
        
        return {'img': observation, 'prev_actions': self.prev_actions, 'state': state}, total_reward, self.done, info
        
        return {'img': observation, 'prev_actions': self.prev_actions, 'state': state}, total_reward, self.done, info
    def reset(self):
        self.done = True
        # 重置血量
        self.rewardGen.reset_health()
        self.rewardGen.death = False
        self.rewardGen.boss_death = False
        self.rewardGen.total_reward = 0
        restart()
        
        self.training_round += 1
        self.action_count = 0
        self.round_rewards = []
        # print(f"Round {self.training_round} starts.")
        
        # self.last_reset_time = time.time()
        # self.ignore_death_time = time.time() + 10  # 忽略接下来10秒的死亡判断
        # time.sleep(2)
        self.first_step = True
        frame = self.grab_screen_shot()
        observation = cv2.resize(frame, (self.model_width, self.model_height))
        health, boss_health, mana = self.calculate_health_and_mana()
        
        # 初始化 prev_actions动作
        self.prev_actions = np.zeros((NUM_ACTION_HISTORY, NUMBER_DISCRETE_ACTIONS), dtype=np.uint8)
        return {'img': observation, 'prev_actions': self.prev_actions, 'state': np.array([health, boss_health, mana])}



    def render(self, mode='human'):
        pass

    def close(self):
        pass
