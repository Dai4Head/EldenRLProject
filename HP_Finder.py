import numpy as np
import cv2
from Screen_Graber import capture_window

def calculate_health_percentage(health_bar_img, color_low, color_high):
    hsv_img = cv2.cvtColor(health_bar_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, color_low, color_high)
    white_pixels = cv2.countNonZero(mask)
    total_pixels = np.prod(health_bar_img.shape[:2])
    return (white_pixels / total_pixels) * 100

def get_health_and_mana(window_title="ELDEN RING™"):
    player_bar_rect = (140, 85, 893, 93)
    boss_bar_rect = (396, 767, 1233, 776)
    player_mana_bar_rect = (140, 100, 795, 104)
    player_hsv_low = np.array([0, 90, 75])
    player_hsv_high = np.array([150, 255, 125])
    boss_hsv_low = np.array([0, 150, 50])
    boss_hsv_high = np.array([10, 255, 200])
    player_mana_hsv_low = np.array([90, 100, 50])
    player_mana_hsv_high = np.array([110, 255, 130])

    full_window_image = capture_window(window_title)
    if full_window_image is None:
        print("Can't catch game window")
        return None, None, None

    player_health_percentage = calculate_health_percentage(
        full_window_image[player_bar_rect[1]:player_bar_rect[3], player_bar_rect[0]:player_bar_rect[2]],
        player_hsv_low, player_hsv_high)
    boss_health_percentage = calculate_health_percentage(
        full_window_image[boss_bar_rect[1]:boss_bar_rect[3], boss_bar_rect[0]:boss_bar_rect[2]],
        boss_hsv_low, boss_hsv_high)
    player_mana_percentage = calculate_health_percentage(
        full_window_image[player_mana_bar_rect[1]:player_mana_bar_rect[3], player_mana_bar_rect[0]:player_mana_bar_rect[2]],
        player_mana_hsv_low, player_mana_hsv_high)

    return player_health_percentage, boss_health_percentage, player_mana_percentage
