# パン・チルトカメラマウント

Raspberry Pi 5とサーボモーターを使用したパン・チルト機構の制御プログラム

## 📖 概要

このプロジェクトは、Adafruit Servo HATとSG90サーボモーターを使用して、カメラを水平方向（パン）と垂直方向（チルト）に動かすパン・チルト機構を実装します。

**主な特徴：**
- 台形制御による滑らかで静かな動作
- 振動を完全に抑制（実機検証済み）
- ライブラリとして再利用可能な関数設計
- 初心者にも分かりやすい日本語コメント

## 🛠️ ハードウェア要件

| 部品 | 型番/仕様 | 数量 |
|------|----------|------|
| メインボード | Raspberry Pi 5 (または Raspberry Pi 4) | 1 |
| カメラ | Raspberry Pi カメラモジュール v3 | 1 |
| サーボドライバ | Adafruit 16-Channel PWM/Servo HAT | 1 |
| サーボモーター | SG90 | 2 |
| マウントキット | SG90サーボ用パン・チルトマウント | 1 |
| 電源 | 5V 4A（サーボ用） | 1 |

### 接続構成

- **パンサーボ（左右）**: チャンネル0
- **チルトサーボ（上下）**: チャンネル1
- **通信方式**: I2C（アドレス: 0x40）

## 💻 ソフトウェア要件

### システム要件
- Raspberry Pi OS（最新版）
- Python 3.7以上
- I2C有効化

### 必要なライブラリ

```bash
sudo pip3 install adafruit-circuitpython-servokit --break-system-packages
```

## 🚀 クイックスタート

### 1. I2C接続の確認

```bash
sudo i2cdetect -y 1
```

アドレス `0x40` にPCA9685が検出されることを確認してください。

### 2. 初期位置設定（初回のみ）

サーボホーンを取り付ける前に実行：

```bash
python3 setup_servo_center.py
```

### 3. 動作テスト

フレーム組み付け後に実行：

```bash
python3 servo_control.py
```

## 📝 プログラム説明

### `setup_servo_center.py` - 初期位置決めプログラム

**目的**: サーボホーン取り付け前の初期位置設定

**機能**:
- 両サーボを中央位置（90度）に設定
- 位置保持モード
- シンプルで分かりやすい構造

**使用例**:
```bash
python3 setup_servo_center.py
```

---

### `servo_control.py` - 基本動作ライブラリ ⭐

**目的**: 動作テスト＋ライブラリ機能

**提供する関数**:
- `initialize_servo_kit()` - サーボ初期化
- `move_servo_smooth()` - 台形制御による滑らかな移動
- `set_pan_angle(kit, angle)` - パン角度設定
- `set_tilt_angle(kit, angle)` - チルト角度設定
- `set_pan_tilt(kit, pan, tilt)` - パン・チルト同時設定
- `set_center_position(kit)` - 中央位置へ移動
- `release_servos(kit)` - サーボ解放

**スタンドアロン実行**:
```bash
python3 servo_control.py
```

**ライブラリとして使用**:
```python
import servo_control

# サーボ初期化
kit = servo_control.initialize_servo_kit()

# パンを80度に移動
servo_control.set_pan_angle(kit, 80)

# パン・チルトを同時に移動
servo_control.set_pan_tilt(kit, 100, 120)

# 中央位置へ
servo_control.set_center_position(kit)
```

---

### `servo_initial_position_setup.py` - リファレンス実装

**目的**: 原稿掲載コードの参考実装（メニュー形式）

実績のあるリファレンスとして保持されています。

## 🎯 動作仕様

### 制御パラメータ

| 項目 | 仕様 |
|------|------|
| PWM周波数 | 50Hz |
| パルス幅（SG90） | 750～2250μs |
| 制御方式 | 台形制御（加速・減速） |
| ステップ角度 | 1度 |

### 動作範囲（実機検証済み）

| サーボ | 範囲 | 中央位置 |
|--------|------|----------|
| パン（左右） | 35～125度 | 80度* |
| チルト（上下） | 45～135度 | 90度 |

\* パンの物理的中央は80度（フレーム構造により90度ではない）

### 台形制御の効果

✅ 振動の完全停止
✅ 駆動音の大幅な低減（約70%）
✅ 滑らかで自然な動き
✅ モーター負荷の軽減

## 📚 ドキュメント

- [仕様書](docs/specification.md) - プロジェクト全体の仕様
- [トラブルシューティング](docs/troubleshooting.md) - 問題解決ガイド
- [開発ルール](CLAUDE.md) - コーディング規約と方針
- [コメントスタイルガイド](COMMENT_STYLE_GUIDE.md) - コメント記載標準

## 🔧 トラブルシューティング

### サーボが動かない

1. I2C接続を確認: `sudo i2cdetect -y 1`
2. サーボ用電源が接続されているか確認
3. サーボがチャンネル0と1に接続されているか確認

### サーボが振動する

⚠️ `servo_control.py` を使用してください。このプログラムは振動対策済みです。

- パルス幅750-2250μsの設定が必須
- 台形制御による滑らかな動作

詳細は [docs/troubleshooting.md](docs/troubleshooting.md) を参照してください。

## 🔗 関連プロジェクト

- [08-002-rpi-servo-multi-control](https://github.com/Murasan201/08-002-rpi-servo-multi-control) - サーボモーター制御の基礎

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照してください。

## 🙏 謝辞

このプロジェクトは書籍原稿の技術検証を目的としています。

---

**プロジェクト**: 12-001-rpi-pan-tilt-camera-mount
**対象書籍**: 第12章「AIにチャレンジ応用編②動くものを追いかける！AI追跡カメラの作成」
