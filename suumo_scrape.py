import requests
import pandas as pd
from io import StringIO
import numpy as np
import sqlite3

# ===== 1. スクレイピング =====
url = "https://suumo.jp/chintai/soba/tokyo/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding

tables = pd.read_html(StringIO(response.text))
df = tables[0]

# 必要な列だけ抽出
df = df.iloc[:, [0, 2]]
df.columns = ["区", "平均家賃（万円）"]

# 欠損値処理 & 数値化
df["平均家賃（万円）"] = (
    df["平均家賃（万円）"]
    .replace("-", np.nan)
    .str.replace("万円", "", regex=False)
    .astype(float)
)

print("=== 取得データ ===")
print(df)

# ===== 2. SQLite に保存 =====
conn = sqlite3.connect("rent.db")

df.to_sql(
    "tokyo_rent",      # テーブル名
    conn,
    if_exists="replace",  # 既存テーブルがあれば上書き
    index=False
)

conn.close()

print("=== DBに保存しました（rent.db）===")
