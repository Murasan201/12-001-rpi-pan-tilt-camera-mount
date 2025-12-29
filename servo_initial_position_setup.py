"""
サーボモーター初期位置設定プログラム

サーボホーンを取り付ける前に実行し、
サーボモーターを中央位置（90度）に設定します。
Ctrl+C で終了できます。
"""

import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C接続とPCA9685の初期化
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# サーボモーターの設定
# チャンネル0: パン（左右）、チャンネル1: チルト（上下）
pan_servo = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2400)
tilt_servo = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400)

print("サーボモーターを中央位置（90度）に設定します...")

# 両サーボを中央位置に移動
pan_servo.angle = 90
tilt_servo.angle = 90

print("設定完了！この状態でサーボホーンを取り付けてください。")
print("Ctrl+C で終了します。")

try:
    # 位置を保持（組付け作業用）
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n終了します。")

finally:
    pca.deinit()
