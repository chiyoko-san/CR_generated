# generate_kimie_banners.py
import os
import time
import base64
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = "kimie_banners"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_PROMPT = """
日本向け化粧品広告バナーを作成。
商品名: KIMIE WRINKLE WHITE PREMIUM
目的: 売れる広告バナー
背景: とても鮮やか、ピンク、ゴールド、透明感、光、ツヤ、上品、高級感
商品: 白いチューブ型スキンケアクリームを中央または右側に大きく配置
訴求: シワ改善、美白ケア、透明感、うるおい、ハリ
日本語コピーを入れる:
「ハリ・透明感ケア」
「薬用シワ改善 × 美白」
「今すぐチェック」
薬機法に配慮し、断定的すぎる表現は避ける。
EC広告・LPファーストビュー向け。
高級感のある美容広告デザイン。
"""

VARIATIONS = [
    "ピンク系で華やか、女性向け、きらめき多め",
    "ゴールド系で高級感、プレミアム感を強調",
    "白とピンクで清潔感、透明感重視",
    "水しぶきと美容液の質感を入れる",
    "セール訴求あり、CTAボタンを目立たせる",
    "口コミ風・満足度風の丸いバッジを入れる",
    "40代以上向けの落ち着いた高級デザイン",
    "SNS広告向けに文字を大きく読みやすく",
    "LPヘッダー向けに横長でインパクト重視",
    "百貨店コスメのような上品な雰囲気",
]

def generate_one(index: int):
    variation = VARIATIONS[index % len(VARIATIONS)]

    prompt = f"""
{BASE_PROMPT}

今回のデザイン方向:
{variation}

画像サイズは横長広告バナー。
文字は読みやすく、商品を美しく目立たせる。
毎回レイアウト、背景、装飾、コピー配置を少し変える。
"""

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/kimie_banner_{index+1:03d}_{timestamp}.png"

    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"saved: {filename}")


def main():
    images_per_day = 100
    interval_seconds = int(24 * 60 * 60 / images_per_day)  # 約864秒 = 14.4分

    for i in range(images_per_day):
        try:
            generate_one(i)
        except Exception as e:
            print(f"error on image {i+1}: {e}")

        if i < images_per_day - 1:
            time.sleep(interval_seconds)


if __name__ == "__main__":
    main()