# Favicon Generator 🎨

JPG画像から複数形式・サイズのファビコンを自動生成するPythonツールです。

## 特徴 ✨

- **10種類のファビコン**を一括生成
- **高品質なリサイズ**処理（LANCZOS算法）
- **背景透過**対応（白背景の自動除去）
- **正方形調整**（縦幅基準でのクロップ）
- **コマンドライン**から簡単操作

## 生成されるファイル 📦

### ICOファイル（4種類）
- `favicon-16.ico` - 16×16px、通常背景
- `favicon-48.ico` - 48×48px、通常背景
- `favicon-16-transparent.ico` - 16×16px、背景透過
- `favicon-48-transparent.ico` - 48×48px、背景透過

### PNGファイル（2種類）
- `apple-touch-icon.png` - 180×180px、通常背景（Apple Touch Icon用）
- `apple-touch-icon-transparent.png` - 180×180px、背景透過

### SVGファイル（4種類）
- `favicon-original.svg` - オリジナルサイズ、通常背景
- `favicon-original-transparent.svg` - オリジナルサイズ、背景透過
- `favicon-square.svg` - 正方形調整、通常背景
- `favicon-square-transparent.svg` - 正方形調整、背景透過

## インストール 📥

```bash
# リポジトリをクローン
git clone <repository-url>
cd create_favicon

# 必要なライブラリをインストール
pip install -r requirements.txt
```

## 使い方 🚀

### 基本的な使い方
```bash
python create_favicon.py input.jpg
```

### オプションを指定
```bash
# 出力ディレクトリを変更
python create_favicon.py input.jpg --output ./my_favicons

# 画像品質を指定（1-100）
python create_favicon.py input.jpg --quality 90

# 透明化の閾値を調整（0-255）
python create_favicon.py input.jpg --transparent-threshold 220
```

### ヘルプを表示
```bash
python create_favicon.py --help
```

## 出力構造 📁

```
output/
└── [入力ファイル名]/
    ├── favicon-16.ico
    ├── favicon-48.ico
    ├── favicon-16-transparent.ico
    ├── favicon-48-transparent.ico
    ├── apple-touch-icon.png
    ├── apple-touch-icon-transparent.png
    ├── favicon-original.svg
    ├── favicon-original-transparent.svg
    ├── favicon-square.svg
    └── favicon-square-transparent.svg
```

## 要件 📋

- Python 3.8+
- Pillow (PIL) 10.0.0+

## 技術仕様 🔧

### 正方形調整
入力画像の縦幅を基準に、横幅も同じサイズに調整（中央クロップ）

### 背景透過
白に近い色（デフォルト: RGB値240以上）を透明に変換

### 高品質リサイズ
LANCZOSアルゴリズムを使用した高品質なリサイズ処理

## 制限事項 ⚠️

- 入力形式: JPGファイルのみ対応
- 最小サイズ: 16×16px以上
- SVG生成: ラスター画像の埋め込み形式（真のベクター化ではありません）

## 例 💡

```bash
# 例: 富士山の画像からファビコンを生成
python create_favicon.py img/mtfuji_in_japanflag.jpg

# 生成結果
# output/mtfuji_in_japanflag/ 以下に10種類のファビコンが作成されます
```

## ライセンス 📄

このツールで生成されたファビコンの著作権は、元画像の著作権に従います。

## 貢献 🤝

バグ報告や機能要望は、Issueまたはプルリクエストでお願いします！