import time
from directkeys import start_boss

# 死亡后重启并走到boss处锁定视角
def restart():
    # print("dead and restart")
    time.sleep(16)
    start_boss()
    time.sleep(1)
    # print("开始新一轮")
  
if __name__ == "__main__":  
    restart()