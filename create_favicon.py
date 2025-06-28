#!/usr/bin/env python3
"""
Favicon Generator - JPG画像から複数形式・サイズのファビコンを自動生成

Usage:
    python create_favicon.py input.jpg
    python create_favicon.py input.jpg --output ./favicons --quality 95
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Tuple, Optional
import logging

try:
    from PIL import Image, ImageFilter
except ImportError as e:
    print(f"❌ エラー: Pillowライブラリがインストールされていません")
    print(f"以下のコマンドを実行してください: pip install Pillow")
    print(f"詳細: {e}")
    sys.exit(1)


class FaviconGenerator:
    """ファビコン生成クラス"""
    
    def __init__(self, quality: int = 95, transparent_threshold: int = 240):
        """
        初期化
        
        Args:
            quality: 画像品質 (1-100)
            transparent_threshold: 透明化の閾値 (0-255)
        """
        self.quality = quality
        self.transparent_threshold = transparent_threshold
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def make_square_crop(self, image: Image.Image) -> Image.Image:
        """
        縦幅を基準とした正方形クロップ（中央切り出し）
        
        Args:
            image: 入力画像
            
        Returns:
            正方形にクロップされた画像
        """
        width, height = image.size
        
        if width == height:
            return image
        
        # 縦幅を基準に正方形にクロップ
        square_size = height
        if width < height:
            # 横幅が短い場合は横幅を基準に
            square_size = width
            top = (height - square_size) // 2
            bottom = top + square_size
            return image.crop((0, top, width, bottom))
        else:
            # 横幅が長い場合は縦幅を基準に（両端カット）
            left = (width - square_size) // 2
            right = left + square_size
            return image.crop((left, 0, right, height))
    
    def make_transparent(self, image: Image.Image) -> Image.Image:
        """
        白背景を透明に変換
        
        Args:
            image: 入力画像
            
        Returns:
            背景が透明化された画像
        """
        # RGBAモードに変換
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        data = image.getdata()
        new_data = []
        
        for item in data:
            # 白に近い色を透明に変換
            if (item[0] > self.transparent_threshold and 
                item[1] > self.transparent_threshold and 
                item[2] > self.transparent_threshold):
                new_data.append((255, 255, 255, 0))  # 完全透明
            else:
                new_data.append(item)
        
        image.putdata(new_data)
        return image
    
    def high_quality_resize(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        高品質リサイズ
        
        Args:
            image: 入力画像
            size: 目標サイズ (width, height)
            
        Returns:
            リサイズされた画像
        """
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def create_ico_files(self, image: Image.Image, output_dir: Path, 
                        transparent: bool = False) -> None:
        """
        ICOファイルを生成
        
        Args:
            image: 入力画像
            output_dir: 出力ディレクトリ
            transparent: 透明化するかどうか
        """
        sizes = [(16, 16), (48, 48)]
        
        for size in sizes:
            processed_image = self.high_quality_resize(image, size)
            
            if transparent:
                processed_image = self.make_transparent(processed_image)
                filename = f"favicon-{size[0]}-transparent.ico"
            else:
                filename = f"favicon-{size[0]}.ico"
            
            output_path = output_dir / filename
            processed_image.save(output_path, format='ICO', quality=self.quality)
            self.logger.info(f"✅ 生成完了: {filename}")
    
    def create_png_files(self, image: Image.Image, output_dir: Path, 
                        transparent: bool = False) -> None:
        """
        PNGファイルを生成 (Apple Touch Icon用)
        
        Args:
            image: 入力画像
            output_dir: 出力ディレクトリ
            transparent: 透明化するかどうか
        """
        size = (180, 180)
        processed_image = self.high_quality_resize(image, size)
        
        if transparent:
            processed_image = self.make_transparent(processed_image)
            filename = "apple-touch-icon-transparent.png"
        else:
            filename = "apple-touch-icon.png"
        
        output_path = output_dir / filename
        processed_image.save(output_path, format='PNG', quality=self.quality, optimize=True)
        self.logger.info(f"✅ 生成完了: {filename}")
    
    def create_svg_files(self, image: Image.Image, output_dir: Path) -> None:
        """
        SVGファイルを生成（画像埋め込み形式）
        
        Args:
            image: 入力画像
            output_dir: 出力ディレクトリ
        """
        # オリジナルサイズのSVG
        self._create_svg_from_image(image, output_dir / "favicon-original.svg", False)
        self._create_svg_from_image(image, output_dir / "favicon-original-transparent.svg", True)
        
        # 正方形調整したSVG
        square_image = self.make_square_crop(image.copy())
        self._create_svg_from_image(square_image, output_dir / "favicon-square.svg", False)
        self._create_svg_from_image(square_image, output_dir / "favicon-square-transparent.svg", True)
    
    def _create_svg_from_image(self, image: Image.Image, output_path: Path, 
                              transparent: bool) -> None:
        """
        画像からSVGファイルを生成
        
        Args:
            image: 入力画像
            output_path: 出力パス
            transparent: 透明化するかどうか
        """
        if transparent:
            image = self.make_transparent(image)
        
        # 一時的にPNGとして保存
        temp_png = output_path.with_suffix('.temp.png')
        image.save(temp_png, format='PNG')
        
        # SVGテンプレート生成
        width, height = image.size
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" 
     viewBox="0 0 {width} {height}">
    <image xlink:href="data:image/png;base64,{self._image_to_base64(temp_png)}" 
           width="{width}" height="{height}"/>
</svg>'''
        
        # SVGファイル保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        # 一時ファイル削除
        temp_png.unlink()
        
        self.logger.info(f"✅ 生成完了: {output_path.name}")
    
    def _image_to_base64(self, image_path: Path) -> str:
        """画像をBase64エンコード"""
        import base64
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def get_output_dir(self, input_path: Path, output_base: str = "output") -> Path:
        """
        出力ディレクトリを取得・作成
        
        Args:
            input_path: 入力ファイルパス
            output_base: 出力ベースディレクトリ
            
        Returns:
            出力ディレクトリパス
        """
        stem = input_path.stem  # 拡張子なしのファイル名
        output_dir = Path(output_base) / stem
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def validate_input(self, input_path: Path) -> bool:
        """
        入力ファイルの検証
        
        Args:
            input_path: 入力ファイルパス
            
        Returns:
            検証結果
        """
        if not input_path.exists():
            self.logger.error(f"❌ エラー: ファイル '{input_path}' が見つかりません")
            return False
        
        if input_path.suffix.lower() not in ['.jpg', '.jpeg']:
            self.logger.error(f"❌ エラー: JPGファイルのみサポートしています (入力: {input_path.suffix})")
            return False
        
        try:
            with Image.open(input_path) as img:
                if img.size[0] < 16 or img.size[1] < 16:
                    self.logger.error(f"❌ エラー: 画像サイズが小さすぎます (最小: 16x16px)")
                    return False
        except Exception as e:
            self.logger.error(f"❌ エラー: 画像ファイルを読み込めません - {e}")
            return False
        
        return True
    
    def generate_favicons(self, input_path: Path, output_base: str = "output") -> bool:
        """
        ファビコンを生成
        
        Args:
            input_path: 入力ファイルパス
            output_base: 出力ベースディレクトリ
            
        Returns:
            成功したかどうか
        """
        if not self.validate_input(input_path):
            return False
        
        self.logger.info(f"🚀 ファビコン生成開始: {input_path.name}")
        
        try:
            # 画像読み込み
            with Image.open(input_path) as original_image:
                # RGBモードに変換（JPGは通常RGBだが念のため）
                if original_image.mode != 'RGB':
                    original_image = original_image.convert('RGB')
                
                # 出力ディレクトリ作成
                output_dir = self.get_output_dir(input_path, output_base)
                self.logger.info(f"📁 出力先: {output_dir}")
                
                # 正方形にクロップした画像を準備
                square_image = self.make_square_crop(original_image.copy())
                
                # ICOファイル生成（通常背景）
                self.create_ico_files(square_image, output_dir, transparent=False)
                
                # ICOファイル生成（透明背景）
                self.create_ico_files(square_image, output_dir, transparent=True)
                
                # PNGファイル生成（通常背景）
                self.create_png_files(square_image, output_dir, transparent=False)
                
                # PNGファイル生成（透明背景）
                self.create_png_files(square_image, output_dir, transparent=True)
                
                # SVGファイル生成
                self.create_svg_files(original_image, output_dir)
                
                self.logger.info(f"🎉 すべてのファビコン生成完了！ ({output_dir})")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ エラー: ファビコン生成中にエラーが発生しました - {e}")
            return False


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="JPG画像から複数形式・サイズのファビコンを自動生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python create_favicon.py input.jpg
  python create_favicon.py input.jpg --output ./favicons
  python create_favicon.py input.jpg --quality 90 --transparent-threshold 220
        """
    )
    
    parser.add_argument(
        'input', 
        type=str, 
        help='入力JPGファイルのパス'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='出力ディレクトリ（デフォルト: output）'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=95,
        help='画像品質 1-100（デフォルト: 95）'
    )
    
    parser.add_argument(
        '--transparent-threshold', '-t',
        type=int,
        default=240,
        help='透明化の閾値 0-255（デフォルト: 240）'
    )
    
    args = parser.parse_args()
    
    # 引数検証
    if not (1 <= args.quality <= 100):
        print("❌ エラー: 品質は1-100の範囲で指定してください")
        sys.exit(1)
    
    if not (0 <= args.transparent_threshold <= 255):
        print("❌ エラー: 透明化閾値は0-255の範囲で指定してください")
        sys.exit(1)
    
    # ファビコン生成実行
    generator = FaviconGenerator(
        quality=args.quality,
        transparent_threshold=args.transparent_threshold
    )
    
    input_path = Path(args.input)
    success = generator.generate_favicons(input_path, args.output)
    
    if success:
        print("\n🎊 ファビコン生成が完了しました！")
        sys.exit(0)
    else:
        print("\n💥 ファビコン生成に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()
