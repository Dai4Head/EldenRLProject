Introduction to code files:
main: The main function, run it to start training the model
Screen_Graber and HP_Finder: Screen-grabbing game windows and calculating the health of characters and bosses in the window
directkeys and getkeys: keyboard mapping and combo writing
restart: specifically controls the re-entry into the boss room after the character resurrects
EldenEnv: Configure the environment step function for training to control each decision, and the reset function is responsible for restarting after the end of word training
EldenReward: Responsible for updating the game state and Reward mechanism
train: Call the environment to start training
The log folder saves the log, and the model folder saves the model. The model is too large to be conveniently uploaded to git.

Training precautions:
1. Set HORIZON_WINDOW to 1000, and train for about an hour each time, with approximately fifty rounds. After training, manually interrupt the process (note that you need to wait until the modelupdated printout appears before interrupting).
2. In this document, enter "The number of training sessions for the model, the model storage time for 'PPO-1.zip' is" during each training session
3. After manually breaking, delete the redundant round data and record the model save time
4. The first training has been completed, so the CREATE_NEW_MODEL code has been changed to False. Next, simply run main
5. After each training session, make sure to backup the latest model before training the next round

Elden Ring environment configuration
(The pictures and materials are in the requirements folder)
1. Instructions for archiving
Game Launch Location: ELDEN RING\Game\eldenring.exe
Archive location: Place the 76561197960267366 folder in the following path.
C:\Users\username\AppData\Roaming\EldenRing\76561197960267366
   1. The folder cannot have Chinese characters, and there cannot be too many folders applied
   2. The system user name cannot be in Chinese
4/4/2024 update for archive:
1. If you cannot find the AppData folder, please check Show hidden files, as shown in the figure
(1712164471098.jpg)
2. If you start the game with STEAM, please replace the save file with the program ERSaveIDEditor.exe:
(1712164753827.png)
2. Description of character status
   Competence Value
(image.png)
Vitality corresponds to blood volume
Concentrated force corresponds to the amount of blue
Endurance corresponds to the green bar, which can be understood as mobility. All actions such as casting/moving/rolling/attacking require endurance, which will automatically regenerate. After reaching the endurance threshold, you can no longer perform any actions except walking
Strength/Dexterity/Faith/Sensing are not required for this training, as they are related to weapon type damage correction (damage correction will be explained in the following text), and are all set to 20
Intelligence corresponds to spell power, set to 99 (image-2.png)
The basic attributes are as follows
HP: 2226
MP: 450
Energy: 170
Memory (Carrying Magic): Meteorite
3. Supplementary knowledge of weapons:
Primary weapon (right hand weapon): The name of the knife is Yueyin
(image-3.png)
Secondary weapon (left hand weapon): Kalia's Scepter
(image-4.png)
The required ability value refers to the fact that if the relevant attribute points are not enough to reach the threshold, the weapon's full performance cannot be exerted and the damage will be very low
Ability bonus refers to the damage correction of relevant attributes, with S being the highest, followed by A, B, C, D, E, and F. When the ability value is S, it means that the higher the attribute, the higher the damage of this weapon. The positive correlation has the highest benefit. When the ability value is F, it means that although the ability value is proportional to the weapon's damage, the benefit is very low and can be ignored
Additional effect: The cumulative bleeding meter of 50 refers to the fact that each effective hit can apply a 50 bleeding debuff to the enemy, and when it reaches 100, the enemy will receive a single massive bleeding damage. However, each character (enemy or friend) has bleeding resistance, so it often takes several cuts to accumulate the full bleeding effect
Attack power refers to the damage that can be inflicted on the enemy, but because the enemy also has physical and magical resistance, it cannot cause the 178+55+213+230 damage on the panel, and the actual damage is about 329 (the light attack of the famous sword Yueyin)
The combat technique can only release the right-hand weapon or two-handed weapon combat technique, so when we carry the right-hand weapon named "Moon Shadow" and the left-hand weapon "Kalia's Scepter", the default release is "Moon Shadow in the Gap" instead of "Turning and Turning"
Spells require a staff to be released, so when the left hand weapon is empty, it is impossible to release spells, and when the blue bar is empty, it is also impossible to release spells
4. Other related configurations
Game brightness: (image-5.png)
   
Window resolution: (image-6.png)
   
Game Quality: (image-7.png)
4/4/2024 update:
Game buttons:
(e731e177e2a527f677dbb32bd6bb580.png)
(013ab6eccc188aa57c40ea3797b1d03.png)
   1. Remember to change to keyboard and mouse operation after entering the game:
(1712165029113.jpg)
   2. There is no borderless windowing or windowing, otherwise keyboard mapping cannot be performed:
(1712165113015.png)