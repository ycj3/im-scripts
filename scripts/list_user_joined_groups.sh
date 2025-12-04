#!/bin/bash

AppKey=$1
BASE_URL="http://a"${AppKey::2}".chat.agora.io/"${AppKey/\#/\/}""

USER_ID=$2
TOKEN=$3

PAGE_SIZE=20
PAGE_NUM=0
TOTAL_GROUPS=0

echo "🔍 Listing all joined chat groups for user: $USER_ID"
while :; do
  echo "Fetching page $PAGE_NUM..."
  RESPONSE=$(curl -s --fail-with-body -X GET \
    -H "Accept: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/chatgroups/user/$USER_ID?pagesize=$PAGE_SIZE&pagenum=$PAGE_NUM")

  if [ $? -ne 0 ]; then
      echo "❌ Failed to fetch data"
      echo $RESPONSE
      exit 1
  fi

    # --- Validate JSON ---
  if ! echo "$RESPONSE" | jq empty 2>/dev/null; then
      echo "❌ Invalid JSON received:"
      echo "$RESPONSE"
      exit 1
  fi

  # 解析群组列表长度
  GROUP_COUNT=$(echo "$RESPONSE" | jq '.entities | length')

  # 如果没有更多群组，停止
  if [[ "$GROUP_COUNT" -eq 0 ]]; then
    echo "No more groups found. Done."
    break
  fi

  # 累加群组数量
  TOTAL_GROUPS=$((TOTAL_GROUPS + GROUP_COUNT))

  # 可选：输出当前页群组ID列表
  echo "$RESPONSE" | jq -r '.entities[] | "Create At: \(.created/1000 | strftime("%Y-%m-%d %H:%M:%S")) | ID: \(.groupId) | Name: \(.name) " '

  # 下一页
  PAGE_NUM=$((PAGE_NUM + 1))
done

echo "✅ Total groups joined: $TOTAL_GROUPS"
