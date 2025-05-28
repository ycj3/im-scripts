package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"strings"
)

var (
	baseURL    string
	token      string
	deleteTime int64
)

func main() {
	initParams()

	if baseURL == "" {
		fmt.Printf("baseUrl is required\n")
		return
	}
	if token == "" {
		fmt.Printf("token is required\n")
		return
	}

	if err := validateBaseURL(baseURL); err != nil {
		panic(fmt.Sprintf("Invalid BaseURL: %v", err))
	}

	cursor := ""
	limit := 10
	for {
		chatrooms, newCursor := queryChatroomList(cursor, limit)

		fmt.Printf("cursor: %s\n", cursor)
		for _, chatroom := range chatrooms {
			chatroom = queryChatroom(chatroom.ID)
			if chatroom.Created > 0 && chatroom.Created < deleteTime {
				fmt.Printf("delete chatroomId %s created %d\n", chatroom.ID, chatroom.Created)
				if chatroom.ID != "" {
					deleteChatroom(chatroom.ID)
				}
			}
		}
		if len(chatrooms) == 0 || newCursor == "" {
			break
		}
		cursor = newCursor
	}

}

func validateBaseURL(rawURL string) error {
	u, err := url.Parse(rawURL)
	if err != nil {
		return fmt.Errorf("failed to parse URL: %v", err)
	}

	// Host pattern: e.g., a41.chat.agora.io
	hostPattern := `^[a-zA-Z0-9-]+\.chat\.agora\.io$`
	matched, _ := regexp.MatchString(hostPattern, u.Host)
	if !matched {
		return fmt.Errorf("invalid host: %s", u.Host)
	}

	// Path must have at least two parts: /OrgName/AppName
	parts := strings.Split(strings.Trim(u.Path, "/"), "/")
	if len(parts) < 2 {
		return fmt.Errorf("path must have at least two parts (e.g., /OrgName/AppName), got: %s", u.Path)
	}

	return nil
}

func queryChatroomList(cursor string, limit int) ([]Chatroom, string) {
	url := fmt.Sprintf("%s/chatrooms?limit=%d&cursor=%s", baseURL, limit, cursor)
	rs, err := HTTPIMGet(url)
	if err != nil {
		fmt.Printf("query chatroom list error: %v\n", err)
		return []Chatroom{}, ""
	}
	var chatroomResponse ChatroomResponse
	err = json.Unmarshal(rs, &chatroomResponse)
	if err != nil {
		fmt.Printf("json unmarshal error: %v\n", err)
		return []Chatroom{}, ""
	}
	return chatroomResponse.Data, chatroomResponse.Cursor
}

func queryChatroom(chatroomId string) Chatroom {
	url := fmt.Sprintf("%s/chatrooms/%s", baseURL, chatroomId)
	rs, err := HTTPIMGet(url)
	if err != nil {
		fmt.Printf("query chatroom error: %v\n", err)
		return Chatroom{}
	}
	var chatroomResponse ChatroomResponse
	err = json.Unmarshal(rs, &chatroomResponse)
	if err != nil {
		fmt.Printf("json unmarshal error: %v\n", err)
		return Chatroom{}
	}
	if len(chatroomResponse.Data) == 0 {
		return Chatroom{}
	}
	return chatroomResponse.Data[0]
}

func deleteChatroom(chatroomId string) {
	url := fmt.Sprintf("%s/chatrooms/%s", baseURL, chatroomId)
	_, err := HTTPDelete(url)
	if err != nil {
		fmt.Printf("delete chatroom error: %v\n", err)
		return
	}
}

func HTTPIMGet(apiURL string) (rs []byte, err error) {
	client := &http.Client{}
	reqest, err := http.NewRequest("GET", apiURL, nil)

	//增加header选项
	reqest.Header.Add("Authorization", fmt.Sprintf("Bearer %s", token))

	resp, err := client.Do(reqest)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return ioutil.ReadAll(resp.Body)
}

func HTTPDelete(apiURL string) (rs []byte, err error) {
	//增加header选项
	client := &http.Client{}
	reqest, err := http.NewRequest("DELETE", apiURL, nil)

	//增加header选项
	reqest.Header.Add("Authorization", fmt.Sprintf("Bearer %s", token))

	resp, err := client.Do(reqest)

	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return ioutil.ReadAll(resp.Body)
}

func initParams() {
	flag.StringVar(&baseURL, "baseURL", "", "rest base URL")
	flag.StringVar(&token, "token", "", "rest access app token")
	flag.Int64Var(&deleteTime, "deleteTime", 0, "delete chatroom before time(millis)")
	flag.Parse()
}

type ChatroomResponse struct {
	Count    int        `json:"count"`
	Data     []Chatroom `json:"data"`
	Duration int        `json:"duration"`
	Cursor   string     `json:"cursor"`
}

type Chatroom struct {
	ID                string `json:"id"`
	Name              string `json:"name"`
	Description       string `json:"description"`
	Membersonly       bool   `json:"membersonly"`
	Allowinvites      bool   `json:"allowinvites"`
	InviteNeedConfirm bool   `json:"invite_need_confirm"`
	Maxusers          int    `json:"maxusers"`
	Owner             string `json:"owner"`
	Created           int64  `json:"created"`
	Custom            string `json:"custom"`
	Mute              bool   `json:"mute"`
	AffiliationsCount int    `json:"affiliations_count"`
	Disabled          bool   `json:"disabled"`
	Public            bool   `json:"public"`
	Permission        string `json:"permission"`
}
