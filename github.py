import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv

load_dotenv()


class Github:
    
    database_filename = os.environ.get('DATABASE')
    db_dir = database_filename.split('/')[0] if len(database_filename.split('/')) > 1 else None
    db_name = database_filename.split('/')[-1] if len(database_filename.split('/')) > 1 else database_filename.split('/')[0]
    
    repo = os.environ.get('DATABASE_REPO')
    user, repo_name = repo.split('/')[0], repo.split('/')[1]
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_url = f'https://{github_token}@github.com/{user}/{repo_name}.git'
    
    BASE_DIR = os.path.dirname(Path(__file__).resolve())
    
    def __init__(self, data=database_filename):
        if not Path(data).exists():
            self.clone()
        else:
            self.pull()
    
    def clone(self):
        try:
            process = subprocess.run(
                ['git', 'clone', self.repo_url, 'data'],
                cwd='.',
                stdout=subprocess.PIPE
            )
            
            if int(process.returncode) != 0:
                print('Command failed. Return code: {}'.format(process.returncode))
                raise(Exception)
        except Exception as e:
            print(e)
            
    def pull(self):
        try:
            process = subprocess.run(
                ['git', 'pull'],
                cwd=Path(self.db_dir).resolve(),
                stdout=subprocess.PIPE
            )
            
            if int(process.returncode) != 0:
                print('Command failed. Return code: {}'.format(process.returncode))
                raise(Exception)
        except Exception as e:
            print(e)

    def upload(self, database=database_filename, message='update'):
        try:
            db_dir = database.split('/')[0] if len(database.split('/')) > 1 else None
            db_name = database.split('/')[-1] if len(database.split('/')) > 1 else database.split('/')[0]

            if Path(db_dir).resolve().exists():
                process = subprocess.run(
                    ['git', 'add', Path(db_name)],
                    cwd=Path(db_dir).resolve(),
                    stdout=subprocess.PIPE
                )

                process = subprocess.run(
                    ['git', 'commit', '-m', message],
                    cwd=Path(db_dir).resolve(),
                    stdout=subprocess.PIPE
                )
                
                process = subprocess.run(
                    ['git', 'push', '-u', 'origin', 'main'],
                    cwd=Path(db_dir).resolve(),
                    stdout=subprocess.PIPE
                )

                if int(process.returncode) != 0:
                    print('Command failed. Return code: {}'.format(process.returncode))
                    raise(Exception)
        except Exception as e:
            print(e)


def main():
    database_filename = os.environ.get('DATABASE')
    db_dir = database_filename.split('/')[0] if len(database_filename.split('/')) > 1 else None
    db_name = database_filename.split('/')[-1] if len(database_filename.split('/')) > 1 else database_filename.split('/')[0]

    gh = Github()
    #gh.upload(db_name)


if __name__ == '__main__':
    main()