import train

if __name__ == '__main__':
    # 模型信息设定
    env_config = {
        "DEBUG_MODE": False,    # 默认调试模式关闭
        "GAME_MODE": "PVE",     # 游戏模式
        # 基础属性设置
        "PLAYER_HP": 2226,
        "PLAYER_MP": 450,
        "DESIRED_FPS": 20       # 设置最高所需的 fps（用于每秒操作数）（20 = 每秒 2 个操作数）
    }
    CREATE_NEW_MODEL = False
         # 创建新模型或恢复现有模型的训练
         

    # 开始训练
    print("EldenRL")
    train.train(CREATE_NEW_MODEL, env_config)