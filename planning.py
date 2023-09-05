import schedule
import time
import os
from broker import InvertirOnline
from supabase_database import SupabaseDatabase
import argparse


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
        
    def execute(self, show=True):
        iol = InvertirOnline()
        data = iol.portafolio()

        db = SupabaseDatabase()
        db.insert_many(data)

        if show:
            self.welcome_message(clear=True)
        
        return True


def main():
    parser = argparse.ArgumentParser(description='Can do actions automatically')

    parser.add_argument('-n', '--now', action='store_true', help='Gets stocks and stores in the database')

    args = parser.parse_args()

    task = Task()
    task.welcome_message()
    
    if args.now:
        task.execute(False)
    else:
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
