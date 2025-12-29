#!/usr/bin/env python3
"""
サーボ初期位置設定プログラム
パン・チルトサーボを中央位置（90度）に設定し、サーボホーン取り付けを支援
要件定義書: docs/specification.md
"""

import time
from adafruit_servokit import ServoKit

# サーボ制御の定数
SERVO_CHANNELS = 16          # サーボHATのチャンネル数
PAN_CHANNEL = 0              # パンサーボ（左右）のチャンネル
TILT_CHANNEL = 1             # チルトサーボ（上下）のチャンネル
PULSE_MIN = 750              # SG90サーボの最小パルス幅（μs）
PULSE_MAX = 2250             # SG90サーボの最大パルス幅（μs）
CENTER_ANGLE = 90            # 中央位置の角度

def initialize_servos():
    """
    サーボモーターの初期化

    ServoKitライブラリを使用してPCA9685チップを制御します。
    SG90サーボに最適なパルス幅（750-2250μs）を設定することで、
    振動を防止し、正確な角度制御を実現します。

    Returns:
        ServoKit: 初期化されたServoKitオブジェクト
    """
    print("サーボモーターを初期化中...")

    # ServoKitの初期化（16チャンネル）
    kit = ServoKit(channels=SERVO_CHANNELS)

    # パルス幅範囲を設定（SG90サーボ用）
    # デフォルト設定では振動が発生するため、明示的に設定が必要
    kit.servo[PAN_CHANNEL].set_pulse_width_range(PULSE_MIN, PULSE_MAX)
    kit.servo[TILT_CHANNEL].set_pulse_width_range(PULSE_MIN, PULSE_MAX)

    print(f"初期化完了（パルス幅: {PULSE_MIN}-{PULSE_MAX}μs）")
    return kit

def set_center_position(kit):
    """
    両サーボを中央位置（90度）に移動

    Args:
        kit (ServoKit): 初期化済みのServoKitオブジェクト
    """
    print(f"\n両サーボを中央位置（{CENTER_ANGLE}度）に移動します...")

    # パンサーボを中央へ
    kit.servo[PAN_CHANNEL].angle = CENTER_ANGLE
    print(f"  パンサーボ（チャンネル{PAN_CHANNEL}）: {CENTER_ANGLE}度")

    # チルトサーボを中央へ
    kit.servo[TILT_CHANNEL].angle = CENTER_ANGLE
    print(f"  チルトサーボ（チャンネル{TILT_CHANNEL}）: {CENTER_ANGLE}度")

    # サーボが位置に到達するまで待機
    time.sleep(1)

    print("\n✓ 移動完了")
    print("この状態でサーボホーンを取り付けてください。")

def main():
    """
    メイン関数：サーボを中央位置に設定してホーン取り付けを支援
    """
    print("=" * 60)
    print("サーボモーター初期位置設定プログラム")
    print("=" * 60)
    print()
    print("このプログラムは、サーボモーターを中央位置（90度）に設定します。")
    print("サーボホーンを取り付ける前に実行してください。")
    print()

    try:
        # サーボの初期化
        kit = initialize_servos()

        # 中央位置へ移動
        set_center_position(kit)

        # 位置保持モード
        print("\n位置を保持しています...")
        print("Ctrl+C を押すと終了します。")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n割り込み信号を受信しました。終了処理を実行中...")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("\n対処方法:")
        print("  1. サーボHATが正しく接続されているか確認")
        print("  2. I2C接続を確認: i2cdetect -y 1")
        print("  3. サーボ用電源が接続されているか確認")

    finally:
        # サーボを解放（振動停止）
        print("\nサーボを解放します...")
        try:
            kit.servo[PAN_CHANNEL].fraction = None
            kit.servo[TILT_CHANNEL].fraction = None
            print("✓ サーボを解放しました")
        except:
            pass

        print("プログラムを終了しました。")

if __name__ == "__main__":
    main()
