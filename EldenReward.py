import cv2
import numpy as np
import time
from HP_Finder import get_health_and_mana
from Screen_Graber import capture_window


class EldenReward:
    def __init__(self, config):
        # pytesseract.pytesseract.tesseract_cmd = config["PYTESSERACT_PATH"]  # 设置PyTesseract路径
        self.DEBUG_MODE = config["DEBUG_MODE"]  # 调试模式
        self.death = False  # 角色是否死亡
        self.boss_death = False  # Boss是否死亡
        self.image_detection_tolerance = 0.02  # 图像检测容忍度
        # self.ignore_death_time = 0 # 解决进房reset问题的一种尝试
        self.last_print_time = time.time()  # 初始化上次打印时间
        
        self.last_boss_hp = 100
        self.last_check_time = time.time()
        self.boss_damage_threshold = 3  # 百分比
        self.boss_penalty_time = 12  # 秒
        self.last_action = None
        self.heal_penalty_threshold = 95
        
        # 初始化血量为满血
        self.curr_hp = 98.8
        self.curr_boss_hp = 98.6
        self.curr_mana = 100
        self.total_reward = 0
        self.boss_last_check = 98.6

    def reset_health(self):
        # 重置血量为100
        self.curr_hp = 98.8
        self.curr_boss_hp = 98.6
        self.curr_mana = 100
        # print("成功重置血量初始化")
        
    def update(self, frame, first_step):
        '''每步调用，返回总奖励，及角色、Boss是否死亡'''
        if first_step: 
            self.time_since_dmg_taken = time.time() - 10  # 初始设置，避免游戏开始时立即获得负面奖励
        curr_time = time.time()
        self.curr_hp, self.curr_boss_hp, self.curr_mana = get_health_and_mana()
        
        # 如果距离上次打印时间超过3秒，则打印当前血量，并更新上次打印时间
        current_time = time.time()
        if current_time - self.last_print_time >= 3:
            # print(f"HP: {self.curr_hp}, Boss: {self.curr_boss_hp}")
            self.last_print_time = current_time  # 更新上次打印时间
            self.boss_last_check = self.last_boss_hp
        # 奖励/惩罚逻辑
        # total_reward = 0
        if first_step:
            self.last_boss_hp = self.curr_boss_hp
            self.last_hp = self.curr_hp
        
        # Boss血量减少奖励
        if self.last_boss_hp - self.curr_boss_hp > 1.5:
            self.total_reward += (self.last_boss_hp - self.curr_boss_hp) * 15
        
        # 角色血量显著下降惩罚
        if ((self.last_hp-self.curr_hp) > 20):  # 假设 last_hp 是上次的血量
            self.total_reward -= 20

        # 检查是否超过时间未能对Boss造成有效伤害
        if curr_time - self.last_check_time > self.boss_penalty_time:
            if (self.last_boss_hp - self.curr_boss_hp) < self.boss_damage_threshold:
                self.total_reward -= 50
            self.last_check_time = curr_time
        
        # 成功回血
        if ((self.curr_hp - self.last_hp) > 15):
            self.total_reward += 20

        # 死亡惩罚
        if self.curr_hp <= 1:
            self.death = True
            self.total_reward -= 400
            self.curr_boss_hp = self.boss_last_check
            # print(f"角色死亡，boss还剩{self.boss_last_check}%血")
            self.total_reward += 20*(98.6-self.boss_last_check)   #boss损失血量奖励
            return round(self.total_reward, 3), self.death, self.boss_death
        
        # Boss死亡奖励
        elif 0.002 < self.curr_boss_hp <= 0.8:
            self.boss_death = True
            self.total_reward += 1000
            self.curr_boss_hp = 0
            return round(self.total_reward, 3), self.death, self.boss_death

        # 高血量时动作为heal时的惩罚
        if self.last_action == 'heal' and self.last_hp > self.heal_penalty_threshold:
            self.total_reward -= 15

        self.last_boss_hp = self.curr_boss_hp
        self.last_hp = self.curr_hp

        return round(self.total_reward, 3), self.death, self.boss_death


# # from EldenReward import EldenReward
# '''测试代码'''
# if __name__ == "__main__":
#     env_config = {
#         # "PYTESSERACT_PATH": r'C:\Program Files\Tesseract-OCR\tesseract.exe',    # 设置 PyTesseract 路径
#         "DEBUG_MODE": False,    # 设置是否渲染 AI 视觉（主要用于调试）
#         "GAME_MODE": "PVE",     # 游戏模式
#         "DESIRED_FPS": 24       # 设置期望的帧率（主要用于动作每秒的数量计算）
#     }
#     reward = EldenReward(env_config)  # 使用配置初始化奖励类

#     # 使用 Screen_Graber.py 中的 capture_window 函数直接捕获游戏窗口图像
#     img = capture_window("ELDEN RING™")
#     if img is None:
#         print("未能成功捕获游戏窗口。")
#     else:
#         # 将捕获的图像从BGRA转换为RGB格式，因为OpenCV主要处理RGB空间的图像
#         frame = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

#         # 首次更新，模拟游戏开始时的状态
#         total_reward, is_dead, is_boss_dead = reward.update(frame, True)
#         print(f"Initial update - Total Reward: {total_reward}, Player Dead: {is_dead}, Boss Dead: {is_boss_dead}")

#         time.sleep(1)  # 模拟游戏中的时间流逝

#         # 第二次更新，模拟游戏中的一个后续步骤
#         total_reward, is_dead, is_boss_dead = reward.update(frame, False)
#         print(f"Second update - Total Reward: {total_reward}, Player Dead: {is_dead}, Boss Dead: {is_boss_dead}")
        