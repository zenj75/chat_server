#
# сообщения протокола Jim
import time

timestamp = time.ctime(time.time())
user = ''
contacts = ''
response_code = ''

presence = {
	"action": "presence",
	"time": timestamp,
	"type": "status",
	"user": {
	"account_name": user,
	"status": "Yep, I am here!"
	}
}

response = {
	"action":  "response",
	"status": response_code,
	"time": timestamp,
	"to": user
}


chat_msg = {
	"action":  "message",
	"time":  timestamp,
	"to":  "#room_name",
	"from":  user,
	"encoding": "ascii",
	"message": "Hi all in this room!"
}

get_contacts = {
	"action":  "get_contacts",
	"time":  timestamp,
	"from":  user,
	"some": "some_text"
}

put_contacts = {
	"action":  "get_contacts",
	"time":  timestamp,
	"to":  user,
	"contacts_list" : contacts
}