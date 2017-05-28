import sys
import fbchat
import getpass
import time
import signal
from io import StringIO

class TimerException(Exception):
    pass

def get_client():
    user, password = None, None
    try:
        with open("./.pass_cache") as fin:
            user = fin.readline()
            password = fin.readline()
    except FileNotFoundError:
        user = input("Username: ")
        password = getpass.getpass()
    return fbchat.Client(user, password)

def trigger(signum, frame):
    raise TimerException() 

def print_messages(messages, info):
    for message in messages:
        message_time = int(message.timestamp) // 1000
        local_time = time.time()
        time_format = "%H:%M" if local_time - message_time < 86400 \
                else "%H:%M on %d/%b/%Y"
        t = time.strftime(time_format, time.localtime(message_time))
        name = info["firstName"] if info["id"] in message.author else "me"
        print("\x1b[1m{0}:\x1b[0m {1}\n{2}\n".format(name, message.body, t))

def chat(client, friend, last_messages = 10, timeout = 2):
    info = client.getUserInfo(friend.uid)
    messages = list(reversed(client.getThreadInfo(friend.uid, last_messages)))
    msg_set = set(map(lambda m: m.message_id, messages))
    print_messages(messages, info)
    signal.signal(signal.SIGALRM, trigger)
    signal.alarm(timeout)
    unread = False
    while True:
        try:
            if unread:
                msg = input()
                unread = False
            else:
                msg = input()
            sent = client.send(friend.uid, msg)
            if not sent:
                print("NOT SENT")
        except TimerException:
            updated = list(reversed(client.getThreadInfo(friend.uid, last_messages)))
            updated_set = set(map(lambda m: m.message_id, updated))
            new_set = updated_set - msg_set
            new_messages = list(filter(lambda m: m.message_id in new_set, updated))
            print_messages(new_messages, info)
            messages = updated
            msg_set = updated_set
            signal.alarm(timeout)
        except KeyboardInterrupt:
            print("Exiting")
            return
        except:
            print("Oops, something went wrong")

def main():
    err = sys.stderr
    sys.stderr = StringIO() 
    client = get_client()
    sys.stderr = err 
    try:
        favs = None
        with open("./.favorites") as fin:
            favs = fin.readlines()
    except FileNotFoundError:
        favs = []
    if len(favs) > 0:
        print("Favorites:")
        for i in range(len(favs)):
            print(i, favs[i])
    name = input("Name to chat with (or fav): ")
    try:
        index = int(name)
        used_fav = True
        if index < len(favs):
            friend = client.getUsers(favs[index])[0]
        else:
            raise ValueError()
    except ValueError:
        friend = client.getUsers(name)[0]
        used_fav = False
    correct = False if input('Correct? {0}: '.format(str(friend))).lower() in \
            ['n', '0', 'no'] else True
    with open("./.favorites", "a") as fout:
        if not used_fav:
            fout.write(name + "\n")
    if correct:
        chat(client, friend)

if __name__ == "__main__":
    main()
