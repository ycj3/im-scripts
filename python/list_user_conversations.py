#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

# -----------------------------
# 配置
# -----------------------------
APPKEY = f"{sys.argv[1]}"  # 从命令行参数获取 AppKey 的第一个部分
BASE_URL = f"http://a{APPKEY[0:2]}.chat.agora.io/{APPKEY.replace('#', '/')}"
USER_ID = sys.argv[2]
TOKEN = sys.argv[3]
LIMIT = 20

# -----------------------------
# 循环分页拉取
# -----------------------------
cursor = ""
total_conversations = 0

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

while True:
    url = f"{BASE_URL}/sdk/user/{USER_ID}/user_channels/list?limit={LIMIT}"
    if cursor:
        url += f"&cursor={cursor}"

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("❌ 请求失败:", resp.status_code, resp.text)
        break

    try:
        data = resp.json()
    except json.JSONDecodeError as e:
        print("❌ 无法解析 JSON:", e)
        break

    channel_infos = data.get("data", {}).get("channel_infos", [])
    print(f"📄 当前页 conversations 数量: {len(channel_infos)}")
    
    # 清理 payload
    for ch in channel_infos:
        if "meta" in ch and "payload" in ch["meta"]:
            ch["meta"]["payload"] = "<removed>"

    # 输出当前页的 channel_id 和 unread_num
    for ch in channel_infos:
        print(f"- create_at: {datetime.fromtimestamp(ch.get('created_at')/1000)}, channel_id: {ch.get('channel_id')}, unread_num: {ch.get('unread_num')}")

    total_conversations += len(channel_infos)

    # 下一页 cursor
    cursor = data.get("data", {}).get("cursor")
    if not cursor:
        break

print(f"✅ 总 conversations 数量: {total_conversations}")
