import schedule
import time
import os
from broker import InvertirOnline
from database import Database
from supabase_database import SupabaseDatabase
from github import Github
from pathlib import Path


class Task:

    def welcome_message(self, cr=False, clear=False):
        if clear:
            if os.name == 'posix':
                os.system('clear')
            elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':
                os.system('cls')

        if cr:
            print('')
        print('[+] Ejecutando InvertirOnline database backup & restore...')
        
    def execute(self):
        #gh = Github()
        
        iol = InvertirOnline()
        data = iol.portafolio()

        #db = Database()
        #db.add_dict_data(data)
        db = SupabaseDatabase()
        db.insert_many(data)

        #gh.upload()
        
        self.welcome_message(clear=True)
        
        return True


def plan():
    task = Task()
    task.welcome_message()
    
    task.execute()

def main():
    task = Task()
    task.welcome_message()

    schedule.every().monday.at('18:20').do(task.execute)
    schedule.every().tuesday.at('18:20').do(task.execute)
    schedule.every().wednesday.at('18:20').do(task.execute)
    schedule.every().thursday.at('18:20').do(task.execute)
    schedule.every().friday.at('18:20').do(task.execute)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        exit(1)

if __name__ == '__main__':
    main()
