## Delete chat rooms

### Usage

```
% go run delete_chatroom.go -h
  -baseURL string
    	rest base URL
  -deleteTime int
    	delete chatroom before time(millis)
  -token string
    	rest access app token
```

### Example

```
go run delete_chatroom.go -baseURL https://a61.chat.agora.io/61717166/1069763 -deleteTime 1748421382693 -token 007******jMwAADA7h48
cursor:
delete chatroomId 274471627849729 created 1741154942551
```