"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: wall_follow.py

Title: Simple Wall Follow

Author: Roo

Purpose: Implement a simple wall following algorithm using the RACECAR's LIDAR sensor.
"""

########################################################################################
# Imports
########################################################################################

import sys

sys.path.insert(1, '../../library')
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
global speed
global angle
global desired_distance # 目標とする壁からの距離
global kp # P制御のゲイン

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle
    global desired_distance
    global kp

    speed = 0.3  # 前進速度
    angle = 0.0  # 初期角度
    desired_distance = 0.5  # 壁からの目標距離 (メートル)
    kp = 2.0     # P制御のゲイン (調整が必要)

    # This tells the car to begin at a standstill
    rc.drive.stop()
    print(">> Wall Follow Lab")

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed
def update():
    global speed
    global angle
    global desired_distance
    global kp

    # Lidarデータを取得
    lidar_data = rc.lidar.get_samples()

    # 右側の壁までの距離を計算 (例: 270度方向のデータを使用)
    # 実際のLidarの向きと壁の位置関係に合わせて調整が必要
    # ここでは、右側（-90度または270度）のLidarデータを使用することを想定
    # Lidarの角度は0度が車の前方、時計回りに増加
    # 270度は車の右側
    right_angle = 30
    right_distance = rc_utils.get_lidar_average_distance(lidar_data, right_angle - 5, right_angle + 5)

    # 壁との距離の誤差を計算
    error = desired_distance - right_distance

    # P制御で角度を調整
    # エラーが大きいほど、より大きく角度を調整
    angle = kp * error

    # 角度を-1から1の範囲にクランプ
    angle = rc_utils.clamp(angle, -1.0, 1.0)

    # 速度と角度を設定
    rc.drive.set_speed_angle(speed, angle)

    # デバッグ情報の表示 (オプション)
    # print(f"Right Distance: {right_distance:.2f}m, Error: {error:.2f}, Angle: {angle:.2f}")


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()