import os
import base64
import random
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_PROMPT = """
日本向けの化粧品広告バナーを作成してください。

商品名:
KIMIE WRINKLE WHITE PREMIUM

目的:
EC広告、LPファーストビュー、SNS広告でクリックされやすい広告バナー。

背景:
とても鮮やか。
高級感のあるピンク、ゴールド、白、透明感、光沢、きらめき、花びら、光の粒、ツヤ感。

商品:
白いチューブ型のスキンケアクリームを目立つ位置に配置。
中央または右側に大きく配置。
高級スキンケア商品のように美しく見せる。

ターゲット:
30代後半から60代女性。
シワ、ハリ、透明感、美白ケア、うるおいに関心がある層。

広告コピー:
以下のような日本語コピーを自然に入れる。
「薬用シワ改善 × 美白ケア」
「ハリ・透明感、印象アップ」
「年齢肌に、プレミアムな一滴」
「今すぐチェック」

注意:
薬機法に配慮し、効果を断定しすぎない。
「必ず消える」「絶対若返る」などの表現は使わない。
文字は読みやすく、広告として完成度を高くする。
"""

VARIATIONS = [
    "ピンク系で華やか。花びらと光の粒を多めに入れる。",
    "ゴールド系で高級感。プレミアム感を強調する。",
    "白とピンクで清潔感。透明感と明るさを重視する。",
    "美容液のしずく、水しぶき、うるおい感を強調する。",
    "CTAボタンを大きくし、今すぐチェックを目立たせる。",
    "口コミ風の丸いバッジを入れる。ただし実在しない数値は使わない。",
    "40代以上向けに落ち着いた高級美容広告にする。",
    "SNS広告向けに文字を大きく、スマホでも読みやすくする。",
    "LPヘッダー風に横長構成で、商品とコピーを大きく見せる。",
    "百貨店コスメのような上品でラグジュアリーな雰囲気にする。",
    "鮮やかな赤ピンク背景で、強いインパクトを出す。",
    "パール、シルク、金箔のような質感を入れる。",
]

def generate_one():
    variation = random.choice(VARIATIONS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    prompt = f"""
{BASE_PROMPT}

今回のデザイン方向:
{variation}

画像形式:
横長広告バナー。
高品質。
鮮やか。
商品が目立つ。
レイアウトは毎回変える。
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

    filename = f"{OUTPUT_DIR}/kimie_banner_{timestamp}.png"

    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"saved: {filename}")

if __name__ == "__main__":
    generate_one()
