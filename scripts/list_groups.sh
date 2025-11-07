#!/bin/bash

BASE_URL="http://a61.chat.agora.io/611063734/1242670"
USER_ID="65d747d227e60e91c1c4393b"
TOKEN="YWMtHdi3yhqeEfC_LuuKkPIVXwAAAAAAAAAAAAAAAAAAAAHiy80WxY9A3r2zdHeG6ZMsAQMAAAGWPb-MRgBPGgDAvz2FhZ4vc90JklmK5JAplJksbX78XdzUzIPeyrestw"

PAGE_SIZE=100
PAGE_NUM=1
TOTAL_GROUPS=0

while :; do
  echo "Fetching page $PAGE_NUM..."
  RESPONSE=$(curl -s -X GET \
    -H "Accept: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/users/$USER_ID/joined_chatgroups?pagesize=$PAGE_SIZE&pagenum=$PAGE_NUM")

  # 解析群组列表长度
  GROUP_COUNT=$(echo "$RESPONSE" | jq '.data | length')

  # 如果没有更多群组，停止
  if [[ "$GROUP_COUNT" -eq 0 ]]; then
    echo "No more groups found. Done."
    break
  fi

  # 累加群组数量
  TOTAL_GROUPS=$((TOTAL_GROUPS + GROUP_COUNT))

  # 可选：输出当前页群组ID列表
  echo "$RESPONSE" | jq -r '.data[].groupid'

  # 下一页
  PAGE_NUM=$((PAGE_NUM + 1))
done

echo "✅ Total groups joined: $TOTAL_GROUPS"
