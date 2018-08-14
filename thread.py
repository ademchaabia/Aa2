import threading, datetime, json, time
from scripts import scripts

class Thread (threading.Thread):
    def __init__(self, job_name, script_name, username, password, bot, chat_id):
        threading.Thread.__init__(self)
        self.job_name = job_name
        self.script_name = script_name
        self.username = username
        self.password = password
        self.bot = bot
        self.chat_id = chat_id 
    
    def run(self):
        start = datetime.datetime.now().replace(microsecond=0)
        self.bot.send_message(self.chat_id, text='InstaPy Bot - {} start at {}'.format(self.name, time.strftime("%X")))
        
        scripts[self.script_name](self.username, self.password)
        
        end = datetime.datetime.now().replace(microsecond=0)
        self.bot.send_message(self.chat_id, text='InstaPy Bot end at {}\nExecution time {}'.format(time.strftime("%X"), end-start))
        
        # Read the last 9 line to get ended status of InstaPy.
        with open('logs/general.log', "r") as f:
            f.seek (0, 2)                   # Seek @ EOF
            fsize = f.tell()                # Get Size
            f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
            lines = f.readlines()           # Read to end

        lines = lines[-9:]                  # Get last 10 lines
        message = ''.join(str(x.replace("INFO - ", "")) for x in lines)
        self.bot.send_message(self.chat_id, text=message)