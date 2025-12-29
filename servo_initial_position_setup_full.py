import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C接続の初期化
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685の初期化
pca = PCA9685(i2c)
pca.frequency = 50

# サーボモーターの設定
# チャンネル0: パン（左右）
# チャンネル1: チルト（上下）
pan_servo = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2400)
tilt_servo = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400)

print("=" * 50)
print("サーボモーター初期位置設定プログラム")
print("=" * 50)
print()
print("このプログラムは、サーボモーターを中央位置（90度）に")
print("設定します。サーボホーンを取り付ける前に実行してください。")
print()
print("操作方法:")
print("1: 両サーボを中央位置（90度）に移動")
print("2: パンサーボの動作テスト")
print("3: チルトサーボの動作テスト")
print("4: 位置保持モード（組付け作業用）")
print("5: プログラム終了")
print()

try:
    while True:
        choice = input("選択してください (1-5): ").strip()

        if choice == "1":
            print("両サーボを中央位置（90度）に移動します...")
            pan_servo.angle = 90
            tilt_servo.angle = 90
            print("完了しました。この状態でサーボホーンを取り付けてください。")

        elif choice == "2":
            print("パンサーボの動作テストを開始します...")
            print("左に移動 (45度)")
            pan_servo.angle = 45
            time.sleep(1)
            print("中央に移動 (90度)")
            pan_servo.angle = 90
            time.sleep(1)
            print("右に移動 (135度)")
            pan_servo.angle = 135
            time.sleep(1)
            print("中央に戻ります (90度)")
            pan_servo.angle = 90
            print("テスト完了")

        elif choice == "3":
            print("チルトサーボの動作テストを開始します...")
            print("下に移動 (45度)")
            tilt_servo.angle = 45
            time.sleep(1)
            print("中央に移動 (90度)")
            tilt_servo.angle = 90
            time.sleep(1)
            print("上に移動 (135度)")
            tilt_servo.angle = 135
            time.sleep(1)
            print("中央に戻ります (90度)")
            tilt_servo.angle = 90
            print("テスト完了")

        elif choice == "4":
            print("位置保持モードに入ります...")
            print("両サーボを中央位置（90度）に設定し、この状態を保持します。")
            pan_servo.angle = 90
            tilt_servo.angle = 90
            print("組付け作業を行ってください。")
            print("Ctrl+C で終了できます。")
            while True:
                time.sleep(1)

        elif choice == "5":
            print("プログラムを終了します...")
            break

        else:
            print("無効な選択です。1-5 の数字を入力してください。")

        print()

except KeyboardInterrupt:
    print("\nプログラムが中断されました")

finally:
    # クリーンアップ
    pca.deinit()
    print("リソースを解放しました")
