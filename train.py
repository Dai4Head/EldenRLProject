# 导入所需的库和模块
from stable_baselines3 import PPO # , A2C  # 从stable_baselines3库导入PPO和A2C算法
import os  # 导入os模块以操作文件和目录
from EldenEnv import EldenEnv  # 从EldenEnv文件导入EldenEnv类

# 定义训练函数，接受是否创建新模型的标志位和配置信息
def train(CREATE_NEW_MODEL, config):
    print("Training will start soon. This can take a while to initialize")  # 打印初始化训练的提示信息

    # 设置训练参数
    TIMESTEPS = 20            # 学习率乘数，这里表示每次学习的时间步数
    HORIZON_WINDOW = 1000     # 在更新模型之前的步数，相当于每次更新模型前的学习步数

    # 创建模型和日志文件的文件夹结构
    model_name = "PPO-1"     # 定义模型名称
    if not os.path.exists(f"models/{model_name}/"):
        os.makedirs(f"models/{model_name}/")
    if not os.path.exists(f"logs/{model_name}/"):
        os.makedirs(f"logs/{model_name}/") 
    models_dir = f"models/{model_name}/"
    logdir = f"logs/{model_name}/"
    model_path = f"{models_dir}/PPO-1"
    print("Folder structure created")

    # 初始化训练环境
    env = EldenEnv(config)  # 创建EldenEnv实例作为训练环境
    print("EldenEnv initialized")  # 打印环境初始化完成的提示信息

    # 创建新模型或加载现有模型
    if CREATE_NEW_MODEL:  # 如果需要创建新模型
        model = PPO('MultiInputPolicy',  # 使用PPO算法，指定策略类型为多输入策略
                    env,                  # 指定训练环境
                    tensorboard_log=logdir,  # 设置TensorBoard日志目录
                    n_steps=HORIZON_WINDOW,  # 设置更新模型前的步数
                    verbose=1,               # 设置日志输出级别
                    device='cpu')            # 设置训练设备为CPU
        print("New Model created")
    else:
        model = PPO.load(model_path, env=env)  # 从指定路径加载模型
        print("Model loaded")

    # 训练循环
    while True:  # 开启无限循环进行训练
        model.learn(total_timesteps=TIMESTEPS,
                    reset_num_timesteps=True,   # 设置是否重置时间步数
                    tb_log_name="PPO",          # 设置TensorBoard日志名称
                    log_interval=1)             # 设置日志记录间隔
        model.save(f"{models_dir}/PPO-1")  # 保存模型
        print("Model updated")
