# servo_control.py 機能仕様書

**バージョン**: 1.4
**作成日**: 2025-12-29
**最終更新**: 2025-12-29
**プロジェクト**: 12-001-rpi-pan-tilt-camera-mount

---

## 1. 概要

本ドキュメントは `servo_control.py` の機能仕様を定義する。
このモジュールは、パン・チルトカメラマウントのサーボモーター制御を行うライブラリである。

---

## 2. 互換性要件

### 2.1 依存プロジェクト

**重要**: 以下のプロジェクトが本モジュールをライブラリとして使用している。

| プロジェクト | 用途 |
|-------------|------|
| [12-002-pet-monitoring-yolov8](https://github.com/Murasan201/12-002-pet-monitoring-yolov8) | ペット監視システム（AI追跡カメラ） |

### 2.2 必須API（変更禁止）

以下の関数は外部プロジェクトから使用されているため、**シグネチャ（引数・戻り値）を変更してはならない**。

| 関数名 | 引数 | 戻り値 |
|--------|------|--------|
| `initialize_servo_kit()` | なし | ServoKit |
| `set_pan_angle(kit, angle, smooth=True)` | kit, angle, smooth | None |
| `set_tilt_angle(kit, angle, smooth=True)` | kit, angle, smooth | None |
| `set_pan_tilt(kit, pan_angle, tilt_angle, smooth=True)` | kit, pan_angle, tilt_angle, smooth | None |
| `set_center_position(kit, smooth=True)` | kit, smooth | None |
| `release_servos(kit)` | kit | None |

### 2.3 必須定数（変更禁止）

以下の定数は外部プロジェクトから参照される可能性があるため、**名前を変更してはならない**。

```python
PAN_CHANNEL, TILT_CHANNEL
PAN_CENTER, PAN_LEFT, PAN_RIGHT
TILT_CENTER, TILT_DOWN, TILT_UP
```

### 2.4 外部プロジェクトからの参照詳細

以下は `12-002-pet-monitoring-yolov8` の各ファイルからの参照状況である。

#### 2.4.1 camera_tracker.py（メイン追跡プログラム）【互換性対象】

**使用関数**:

| 関数 | 用途 |
|------|------|
| `initialize_servo_kit()` | サーボHAT初期化 |
| `set_pan_angle(kit, angle, smooth)` | パンサーボ制御（P制御追跡時は`smooth=False`） |
| `set_tilt_angle(kit, angle, smooth)` | チルトサーボ制御（P制御追跡時は`smooth=False`） |
| `set_center_position(kit)` | 初期化・リセット時に中央位置へ移動 |
| `release_servos(kit)` | 終了時のクリーンアップ |

**使用定数**:

| 定数 | 用途 |
|------|------|
| `PAN_CENTER`, `TILT_CENTER` | 初期位置・リセット位置 |
| `PAN_LEFT`, `PAN_RIGHT` | スキャン時の左右境界 |
| `TILT_DOWN`, `TILT_UP` | スキャン時の上下境界 |

#### 2.4.2 hold_servo_position.py（サーボ位置固定ツール）【互換性対象】

**使用関数**:

| 関数 | 用途 |
|------|------|
| `initialize_servo_kit()` | サーボHAT初期化 |
| `set_pan_tilt(kit, pan, tilt, smooth)` | 指定位置へ移動 |
| `release_servos(kit)` | サーボ解放（トルクOFF） |

**使用定数**:

| 定数 | 用途 |
|------|------|
| `PAN_CENTER`, `TILT_CENTER` | デフォルト角度値 |
| `PAN_LEFT`, `PAN_RIGHT` | 角度範囲の表示 |
| `TILT_DOWN`, `TILT_UP` | 角度範囲の表示 |
| `PAN_CHANNEL`, `TILT_CHANNEL` | PWM直接制御時のチャンネル指定 |

#### 2.4.3 test_pan_tilt_range.py（可動域テスト）【互換性対象外】

> **注記**: 書籍には掲載しないため、互換性の考慮対象から除外する。

#### 2.4.4 test_tilt_servo.py（チルトサーボ単体テスト）【互換性対象外】

> **注記**: 書籍には掲載しないため、互換性の考慮対象から除外する。

---

## 3. MVP版ライブラリ仕様

### 3.1 必須関数（変更禁止）

互換性対象ファイル（camera_tracker.py, hold_servo_position.py）から使用されている関数。

| 関数 | シグネチャ | 説明 |
|------|-----------|------|
| `initialize_servo_kit()` | `() -> ServoKit` | サーボHAT初期化 |
| `set_pan_angle()` | `(kit, angle, smooth=True) -> None` | パンサーボ移動 |
| `set_tilt_angle()` | `(kit, angle, smooth=True) -> None` | チルトサーボ移動 |
| `set_pan_tilt()` | `(kit, pan_angle, tilt_angle, smooth=True) -> None` | 両サーボ同時移動 |
| `set_center_position()` | `(kit, smooth=True) -> None` | 中央位置へ移動 |
| `release_servos()` | `(kit) -> None` | サーボ解放 |

### 3.2 必須定数（変更禁止）

| 定数 | 値 | 用途 |
|------|-----|------|
| `PAN_CHANNEL` | 0 | パンサーボのチャンネル番号 |
| `TILT_CHANNEL` | 1 | チルトサーボのチャンネル番号 |
| `PAN_CENTER` | 80 | パンサーボの中央位置 |
| `PAN_LEFT` | 35 | パンサーボの左端 |
| `PAN_RIGHT` | 125 | パンサーボの右端 |
| `TILT_CENTER` | 90 | チルトサーボの中央位置 |
| `TILT_DOWN` | 45 | チルトサーボの下端 |
| `TILT_UP` | 120 | チルトサーボの上端 |

### 3.3 必須内部機能（削除不可）

| 機能 | 理由 |
|------|------|
| 台形制御（`smooth=True`時の動作） | camera_tracker.pyで`set_center_position()`等がデフォルト引数（`smooth=True`）で呼び出されており、台形制御が実際に使用されている |

> **注意**: `move_servo_smooth()`関数自体は内部関数のため名前変更や実装簡略化は可能だが、`smooth=True`時に滑らかに移動する機能は維持すること。

### 3.4 残すべき機能（書籍掲載用）

| 機能 | 理由 |
|------|------|
| `main()` | スタンドアロン実行での動作テスト用。書籍原稿に含まれる |
| 基本動作テスト | パン・チルトの動作確認。書籍原稿に含まれる |

> **簡略化可能**: テストパターンの削減、複合テスト（`test_pan_tilt_combined`）の削除は可。

### 3.5 削除可能な機能

| 機能 | 理由 |
|------|------|
| `test_pan_tilt_combined()` | 10パターンの複合テスト。書籍掲載には冗長 |
| 詳細なdocstring | 初心者向けに簡潔化可能 |
| 詳細なエラーメッセージ | 簡潔化可能 |

### 3.6 簡略化可能な機能

以下の機能は残すが、実装を簡略化してよい。

| 機能 | 簡略化の内容 |
|------|-------------|
| `test_pan_servo()` | テストパターンの削減（例：左端→中央→右端→中央 を 中央→左端→右端→中央 に簡略化など） |
| `test_tilt_servo()` | テストパターンの削減 |
| `move_servo_smooth()` | 関数名の変更可、実装の簡略化可（ただし`smooth=True`時の滑らか移動機能は維持） |
| `main()` | 出力メッセージの簡略化、待機モードの簡略化 |

---

## 4. MVP化まとめ

### 4.1 必須機能（削除不可）

| カテゴリ | 内容 |
|---------|------|
| 公開API関数（6つ） | `initialize_servo_kit`, `set_pan_angle`, `set_tilt_angle`, `set_pan_tilt`, `set_center_position`, `release_servos` |
| 定数（8つ） | `PAN_CHANNEL`, `TILT_CHANNEL`, `PAN_CENTER`, `PAN_LEFT`, `PAN_RIGHT`, `TILT_CENTER`, `TILT_DOWN`, `TILT_UP` |
| 台形制御 | `smooth=True`時の滑らか移動機能（camera_tracker.pyで使用） |
| 動作テスト | `main()`によるスタンドアロン実行、基本動作テスト（書籍掲載） |

### 4.2 削除可能

| 機能 |
|------|
| `test_pan_tilt_combined()`（10パターンの複合テスト） |
| 詳細なdocstring |
| 詳細なエラーメッセージ |

### 4.3 簡略化可能

| 機能 |
|------|
| `test_pan_servo()`, `test_tilt_servo()`（テストパターン削減） |
| `move_servo_smooth()`（関数名変更・実装簡略化可、機能は維持） |
| `main()`（出力メッセージ簡略化） |

---

## 5. ハードウェア仕様

### 5.1 接続構成

| 項目 | 仕様 |
|------|------|
| サーボドライバ | Adafruit PCA9685 |
| パンサーボ | チャンネル0 |
| チルトサーボ | チャンネル1 |
| 通信 | I2C（0x40） |
| PWM周波数 | 50Hz |

### 5.2 動作範囲

| サーボ | 範囲 | 中央 |
|--------|------|------|
| パン | 35～125度 | 80度 |
| チルト | 45～120度 | 90度 |

### 5.3 パルス幅

| 項目 | 値 |
|------|-----|
| 最小 | 750μs |
| 最大 | 2250μs |

---

## 6. 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0 | 2025-12-29 | 初版作成、互換性要件を定義 |
| 1.1 | 2025-12-29 | 外部プロジェクトからの参照詳細を追加 |
| 1.2 | 2025-12-29 | テストファイルを互換性対象外に変更、MVP版ライブラリ仕様を定義 |
| 1.3 | 2025-12-29 | 台形制御を必須機能に修正、動作テストを残すべき機能に追加 |
| 1.4 | 2025-12-29 | 簡略化可能な機能セクション追加、MVP化まとめセクション追加 |
