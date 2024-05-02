import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

#第一步是设置键盘映射码

#操作
W = 0x11 # 移动前
A = 0x1E # 移动左
S = 0x1F # 移动后
D = 0x20 # 移动右
V = 0x2F # 用V代替闪避，默认后跳， ＋方向键为翻滚闪避
LSHIFT = 0x2A # 左Shift，+鼠标左键 = 重攻击
R = 0x13 # R键，血瓶
E = 0x12 # E键，互动
F = 0x21 # F键，跳跃
Q = 0x10 # Q键，锁定视角
J = 0x24 # J键，轻攻击
K = 0x25 # K键，重攻击
L = 0x26 # L键，战技技能3

#用于暂停
ESC = 0x01 #菜单
DOWN = 0xD0 #↓
G = 0x22 

#第二步，调包来实现模拟键盘的输入
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
#第三步来实现各个操作的函数，训练模型里调用指定函数代表具体的操作
    
#轻攻击
def attack():
    PressKey(J)
    time.sleep(0.05)
    ReleaseKey(J)
    time.sleep(0.1)
#法术。释放时间较长
def attack2():
    PressKey(K)
    time.sleep(0.05)
    ReleaseKey(K)
    time.sleep(2)

#战技+攻击触发
def attack3():
    PressKey(L)
    time.sleep(0.7)
    PressKey(J)
    time.sleep(0.5)
    ReleaseKey(L)
    ReleaseKey(J)
    time.sleep(0.1)

#重攻击
def attack4():
    PressKey(LSHIFT)
    time.sleep(1)
    PressKey(J)
    time.sleep(1)
    ReleaseKey(LSHIFT)
    ReleaseKey(J)
    time.sleep(0.1)

#移动    
def go_forward():
    # print("go_forward: start")
    PressKey(W)
    time.sleep(0.4)
    ReleaseKey(W)
    # print("go_forward: end")
    
def go_back():
    PressKey(S)
    time.sleep(0.4)
    ReleaseKey(S)
    
def go_left():
    PressKey(A)
    time.sleep(0.4)
    ReleaseKey(A)
    
def go_right():
    PressKey(D)
    time.sleep(0.4)
    ReleaseKey(D)
    
def jump():
    PressKey(F)
    time.sleep(0.1)
    ReleaseKey(F)
    time.sleep(0.1) #避免有的时候衔接不上其他动作

def forward_jump():
    PressKey(W)
    time.sleep(0.4)
    PressKey(F)
    time.sleep(0.8)
    ReleaseKey(W)
    ReleaseKey(F)

#闪避   
def dodge():
    PressKey(V)
    time.sleep(0.3)
    ReleaseKey(V)

def forward_dodge():
    PressKey(W)
    time.sleep(0.2)
    PressKey(V)
    time.sleep(0.1)
    ReleaseKey(V)
    time.sleep(0.3)
    ReleaseKey(W)

def back_dodge():
    PressKey(S)
    time.sleep(0.2)
    PressKey(V)
    time.sleep(0.1)
    ReleaseKey(V)
    time.sleep(0.3)
    ReleaseKey(S)

def left_dodge():
    PressKey(A)
    time.sleep(0.2)
    PressKey(V)
    time.sleep(0.1)
    ReleaseKey(V)
    time.sleep(0.3)
    ReleaseKey(A)


def right_dodge():
    PressKey(D)
    time.sleep(0.2)
    PressKey(V)
    time.sleep(0.1)
    ReleaseKey(V)
    time.sleep(0.3)
    ReleaseKey(D)

#锁视角  
def lock_vision():
    PressKey(Q)
    time.sleep(0.3)
    ReleaseKey(Q)
    time.sleep(0.1)
    
def go_forward_QL(t):
    PressKey(W)
    time.sleep(t)
    ReleaseKey(W)
    
#死了啥也不用摁，自动复活
# def dead():
#     PressKey()
#     time.sleep(0.5)
#     ReleaseKey()


#从篝火走到开BOSS，锁定视角
def start_boss():
    PressKey(W)
    time.sleep(15)
    ReleaseKey(W)
    time.sleep(1)

    PressKey(E)
    time.sleep(0.1)
    ReleaseKey(E)
    time.sleep(3)

    PressKey(Q)
    time.sleep(0.1)
    ReleaseKey(Q)
    time.sleep(1)
    # PressKey(W)
    # time.sleep(15)
    # ReleaseKey(W)
    # time.sleep(1)

    # PressKey(E)
    # time.sleep(0.1)
    # ReleaseKey(E)
    # time.sleep(2.5)
    
    # PressKey(W)
    # time.sleep(4.5)
    # ReleaseKey(W)
    # time.sleep(0.5)
    
    # PressKey(E)
    # time.sleep(0.1)
    # ReleaseKey(E)
    # time.sleep(2.5)

    # PressKey(Q)
    # time.sleep(0.1)
    # ReleaseKey(Q)
    # time.sleep(1)

#暂停用于应对突发情况，游戏没有暂停键（得装MOD)，所以找了另一个办法
def pause_game():
    PressKey(ESC)
    time.sleep(0.1)
    ReleaseKey(ESC)
    PressKey(DOWN)
    time.sleep(0.1)
    ReleaseKey(DOWN)
    PressKey(DOWN)
    time.sleep(0.1)
    ReleaseKey(DOWN)
    PressKey(E)
    time.sleep(0.1)
    ReleaseKey(E)
    PressKey(G)
    time.sleep(0.1)
    ReleaseKey(G)
    PressKey(DOWN)
    time.sleep(0.1)
    ReleaseKey(DOWN)
    PressKey(DOWN)
    time.sleep(0.2)
    ReleaseKey(DOWN)
    PressKey(E)
    time.sleep(0.1)
    ReleaseKey(E)
    
def heal():
    PressKey(R)
    time.sleep(1)
    ReleaseKey(R)

if __name__ == '__main__':
    #开始发呆一会，趁此机会切屏进游戏
    time.sleep(5)

#按键测试
    jump()
    time.sleep(2)
    forward_jump()
    time.sleep(2)
    go_left() 
    go_right()
    go_back() 
    go_forward()
    time.sleep(2)

    dodge()
    left_dodge()
    forward_dodge()
    right_dodge()
    time.sleep(1)
    back_dodge()
    time.sleep(3)
  
    lock_vision()
    time.sleep(1)

    attack()
    time.sleep(1)
    attack2()
    time.sleep(3)
    attack3()
    time.sleep(3)
    attack4()
    time.sleep(3)
    heal()
