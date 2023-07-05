import datetime

if __name__ == "__main__":
    now = datetime.datetime.now().timestamp()
    today = datetime.datetime.fromtimestamp(now).date()
    timestamp = 1688451127
    timedate = datetime.datetime.fromtimestamp(timestamp).date()
    print(today)
    print(timedate)




