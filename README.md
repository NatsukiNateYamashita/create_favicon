# Favicon Generator 🎨

JPG画像から複数形式・サイズのファビコンを自動生成するPythonツールです。

## 特徴 ✨

- **10種類のファビコン**を一括生成
- **高品質なリサイズ**処理（LANCZOSアルゴリズム）
- **背景透過**対応（白背景の自動除去）
- **正方形調整**（縦幅基準でのクロップ）
- **コマンドライン**から簡単操作
- **入力ファイル名ごと**のフォルダ整理

## ファイル構成 📁

```
create_favicon/
├── create_favicon.py          # メインスクリプト
├── requirements.txt           # 依存関係
├── README.md                 # プロジェクト説明（このファイル）
├── .github/
│   └── .copilot_instructions.md # 開発者向けガイド
├── img/                      # サンプル画像
│   └── mtfuji_in_japanflag.jpg
├── output/                   # 生成されたファビコン（自動作成）
│   ├── [画像名1]/
│   │   ├── favicon-16.ico
│   │   ├── favicon-48.ico
│   │   ├── ... (各種ファビコン)
│   └── [画像名2]/
│       └── ... (各種ファビコン)
└── test_image_with_white_bg.jpg # テスト用画像（自動生成）
```

## 生成されるファイル 📦

### ICOファイル（4種類）
| ファイル名 | サイズ | 背景 | 用途 |
|------------|--------|------|------|
| `favicon-16.ico` | 16×16px | 通常 | ブラウザタブ・お気に入り |
| `favicon-48.ico` | 48×48px | 通常 | デスクトップショートカット |
| `favicon-16-transparent.ico` | 16×16px | 透過 | 透明背景対応ブラウザ |
| `favicon-48-transparent.ico` | 48×48px | 透過 | 透明背景対応デスクトップ |

### PNGファイル（2種類）
| ファイル名 | サイズ | 背景 | 用途 |
|------------|--------|------|------|
| `apple-touch-icon.png` | 180×180px | 通常 | iOS・Androidホーム画面 |
| `apple-touch-icon-transparent.png` | 180×180px | 透過 | 透明背景対応モバイル |

### SVGファイル（4種類）
| ファイル名 | サイズ | 背景 | 処理 |
|------------|--------|------|------|
| `favicon-original.svg` | オリジナル | 通常 | サイズそのまま |
| `favicon-original-transparent.svg` | オリジナル | 透過 | サイズそのまま |
| `favicon-square.svg` | 正方形調整 | 通常 | 縦幅基準でクロップ |
| `favicon-square-transparent.svg` | 正方形調整 | 透過 | 縦幅基準でクロップ |

## インストール 📥

### 1. リポジトリをクローン
```bash
git clone <repository-url>
cd create_favicon
```

### 2. 必要なライブラリをインストール
```bash
pip install -r requirements.txt
```

### 3. 動作確認
```bash
python create_favicon.py --help
```

## 使い方 🚀

### 基本的な使い方
```bash
python create_favicon.py input.jpg
```

### コマンドオプション詳細

#### `-h, --help`
ヘルプメッセージを表示します。
```bash
python create_favicon.py --help
```

#### `-o, --output OUTPUT`
出力ディレクトリを指定します（デフォルト: `output`）。
```bash
# カスタムディレクトリに出力
python create_favicon.py input.jpg --output ./my_favicons

# 絶対パスでも指定可能
python create_favicon.py input.jpg -o /path/to/favicons
```

#### `-q, --quality QUALITY`
画像品質を1-100で指定します（デフォルト: 95）。
```bash
# 高品質（ファイルサイズ大）
python create_favicon.py input.jpg --quality 100

# 標準品質
python create_favicon.py input.jpg --quality 85

# 圧縮重視（ファイルサイズ小）
python create_favicon.py input.jpg -q 70
```

#### `-t, --transparent-threshold THRESHOLD`
背景透過の閾値を0-255で指定します（デフォルト: 240）。
```bash
# より厳しい透過（ほぼ純白のみ）
python create_favicon.py input.jpg --transparent-threshold 250

# より緩い透過（グレーっぽい色も透過）
python create_favicon.py input.jpg -t 200
```

### 使用例 💡

#### パターン1: 基本的な使用
```bash
python create_favicon.py logo.jpg
```
**結果**: `output/logo/` に10種類のファビコンが生成

#### パターン2: 高品質・カスタム出力先
```bash
python create_favicon.py company_logo.jpg \
  --output ./website/favicons \
  --quality 100
```
**結果**: `./website/favicons/company_logo/` に高品質ファビコンが生成

#### パターン3: 白背景の厳密な透過
```bash
python create_favicon.py product_image.jpg \
  --transparent-threshold 250 \
  --quality 90
```
**結果**: ほぼ純白のみを透過処理

#### パターン4: 複数画像の処理
```bash
# 複数のファイルを順次処理
python create_favicon.py image1.jpg
python create_favicon.py image2.jpg
python create_favicon.py image3.jpg
```

## 出力構造 📁

```
output/                          # 出力ベースディレクトリ
└── [入力ファイル名]/              # 各画像専用フォルダ
    ├── favicon-16.ico           # 16px ICO（通常背景）
    ├── favicon-48.ico           # 48px ICO（通常背景）
    ├── favicon-16-transparent.ico        # 16px ICO（透過背景）
    ├── favicon-48-transparent.ico        # 48px ICO（透過背景）
    ├── apple-touch-icon.png              # 180px PNG（通常背景）
    ├── apple-touch-icon-transparent.png  # 180px PNG（透過背景）
    ├── favicon-original.svg              # オリジナルサイズ SVG（通常背景）
    ├── favicon-original-transparent.svg  # オリジナルサイズ SVG（透過背景）
    ├── favicon-square.svg               # 正方形調整 SVG（通常背景）
    └── favicon-square-transparent.svg   # 正方形調整 SVG（透過背景）
```

### 実際の例
```
output/
├── mtfuji_in_japanflag/
│   ├── favicon-16.ico
│   ├── favicon-48.ico
│   └── ... (10ファイル)
└── company_logo/
    ├── favicon-16.ico
    ├── favicon-48.ico
    └── ... (10ファイル)
```

## 要件 📋

- **Python**: 3.8以上
- **Pillow (PIL)**: 10.0.0以上
- **OS**: Windows・macOS・Linux対応

## 技術仕様 🔧

### 正方形調整アルゴリズム
1. **縦幅基準**: 入力画像の高さを基準サイズとする
2. **中央クロップ**: 横幅が長い場合、左右を均等にカット
3. **横幅基準**: 横幅が短い場合、上下を均等にカット

```
例: 1200×800の画像
→ 800×800にクロップ（左右200pxずつカット）
```

### 背景透過処理
白に近い色を透明に変換する処理です。

**判定条件**:
```python
if (R > threshold and G > threshold and B > threshold):
    # 透明にする
```

**デフォルト閾値**: 240
- **240**: やや白っぽい色も透過
- **250**: ほぼ純白のみ透過
- **200**: グレーっぽい色も透過

### 高品質リサイズ
**LANCZOSアルゴリズム**を使用した高品質なリサイズ処理。
- **シャープネス**: エッジが鮮明
- **色再現性**: 色の劣化を最小限に抑制
- **処理速度**: やや時間がかかるが品質重視

## 制限事項 ⚠️

### 入力制限
- **対応形式**: JPGファイルのみ（JPEG拡張子含む）
- **最小サイズ**: 16×16px以上
- **推奨サイズ**: 256×256px以上（高品質な結果のため）

### 透過処理の注意点
- **白背景専用**: 現在は白系統の色のみ透過対応
- **グラデーション**: 白からの自然なグラデーションは部分的に残る場合あり
- **JPEG特性**: JPEG圧縮により、純白でない可能性あり

### SVG生成の制限
- **ラスター埋め込み**: 真のベクター化ではなく、画像埋め込み形式
- **ファイルサイズ**: 元画像によっては大きくなる場合あり

## トラブルシューティング 🛠️

### エラー: "ファイルが見つかりません"
```bash
❌ エラー: ファイル 'input.jpg' が見つかりません
```
**解決策**: 
- ファイルパスを確認
- 現在のディレクトリを確認（`pwd`コマンド）
- 絶対パスで指定

### エラー: "JPGファイルのみサポート"
```bash
❌ エラー: JPGファイルのみサポートしています (入力: .png)
```
**解決策**: 
- JPG/JPEG形式に変換してから使用
- 他の形式対応は今後の機能拡張予定

### エラー: "画像サイズが小さすぎます"
```bash
❌ エラー: 画像サイズが小さすぎます (最小: 16x16px)
```
**解決策**: 
- より大きなサイズの画像を使用
- 元画像をアップスケールしてから使用

### 透過処理が効かない
**原因**: 元画像に透過すべき白背景が存在しない
**確認方法**: 
```bash
# テスト用白背景画像で確認
python -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (100, 100), 'white')
draw = ImageDraw.Draw(img)
draw.ellipse([25, 25, 75, 75], fill='red')
img.save('test_white_bg.jpg')
"
python create_favicon.py test_white_bg.jpg
```

## 将来の拡張予定 🚀

- [ ] **PNG・WebP入力**対応
- [ ] **カスタム背景色**の透過処理
- [ ] **バッチ処理**（複数ファイル一括処理）
- [ ] **真のベクターSVG**生成
- [ ] **Web UI版**
- [ ] **カスタムサイズ**指定機能

## ライセンス 📄

このツールは自由に使用できますが、生成されたファビコンの著作権は元画像の著作権に従います。

## 貢献・サポート 🤝

- **バグ報告**: Issue作成
- **機能要望**: Issue作成
- **プルリクエスト**: 歓迎
- **質問**: Discussionsで

---
作成者: あなたの親切なギャルエンジニア 💝