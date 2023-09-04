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
        fecha_hora_actual = datetime.now()

        # formatear la fecha y hora como una cadena para usar como nombre de archivo
        formato = '%Y-%m-%d_%H-%M-%S'  # Cambia el formato según tus necesidades
        nombre_archivo = fecha_hora_actual.strftime(formato)

        return nombre_archivo
    
    def _get_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def current_datetime(self):
        fecha_hora_actual = datetime.now()
        hora = fecha_hora_actual.astimezone(
         pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%H:%M')

        return f'[{hora} hs]'
        
    def count(self):
        return self.supabase.table(self.table).select('count').execute()
    
    def get_following_id(self):
        return self.count().data[0]['count'] + 1
    
    def insert(self, record):
        return self.supabase.table(self.table).insert(record).execute()

    def delete(self, field, value):
        self.supabase.table(self.table).delete().eq(field, value).execute()
        
    def insert_many(self, data, show=True):
        for i, record in enumerate(data):
            self.insert(record)
            
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
    
    
def main():
    db = SupabaseDatabase()
    id = db.get_following_id()
    date = db._get_date()
    records = []
    for i, x in enumerate(range(10)):
        records.append(db.test_record(i + 10, date))
    db.insert_many(records)

if '__main__' == __name__:
    main()
