from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import pytz
import os


load_dotenv()


class SupabaseDatabase:
    
    def __init__(self) -> None:
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_APIKEY")

        self.supabase: Client = create_client(self.url, self.key)

        self.table = 'stocks'
        
    def _generate_timestamp(self):
        '''Gets current date and time'''
        current_datatime = datetime.now()

        format = '%Y-%m-%d_%I-%M-%S_%p'.lower()
        filename = current_datatime.strftime(format)

        return filename
    
    def _get_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def current_datetime(self):
        current_datatime = datetime.now()
        time_now = current_datatime.astimezone(pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%I:%M %p')

        return f'[{time_now}]'
        
    def count(self):
        return self.supabase.table(self.table).select('count').execute()
    
    def get_following_id(self):
        return self.count().data[0]['count'] + 1
    
    def insert(self, record):
        return self.supabase.table(self.table).insert(record).execute()

    def delete(self, field, value):
        self.supabase.table(self.table).delete().eq(field, value).execute()
        
    def insert_many(self, data, show=True):
        self.supabase.table(self.table).upsert(data).execute()
            
        if len(data) > 1:
            print(f'{self.current_datetime()} Saved {len(data)} records')
        else:
            print(f'{self.current_datetime()} Saved {len(data)} record')
        
    def test_record(self, id, date):
        record = {
            "id": id,
            "fecha": date,
            "descripcion": "XApple",
            "ultimo_precio": 14178,
            "cantidad": 33,
            "moneda": "peso_Argentino",
            "ganancia_porcentaje": 57.5,
            "valorizado": 467874,
            "simbolo": "AAPL",
            "variacion_diaria": 2.75,
            "ganancia": 170815
        }
        
        return record
