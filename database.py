import sqlite3
import pytz
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Database:

    database_filename = os.environ.get('DATABASE')
    db_dir = database_filename.split('/')[0] if len(database_filename.split('/')) > 1 else None
    db_name = database_filename.split('/')[-1] if len(database_filename.split('/')) > 1 else database_filename.split('/')[0]
    
    BASE_DIR = os.path.dirname(Path(__file__).resolve())
    db_path = os.path.join(BASE_DIR, db_name)
    
    conn = None
    cursor = None

    def __init__(self, database=database_filename):
        if not Path(database).exists():
            print('No database founded')
            
            try:
                self.conn = self.create_connection(database, True)

                self.create_table('stocks')
            except Exception as e:
                print(e)
        else:
            return None

    def create_connection(self, db_filename=Path(database_filename).resolve(), show=False):
        try:
            if not Path(db_filename).exists():
                print('Database created')

            if show:
                print(f'Database connection established [{db_filename}]')
            self.conn = sqlite3.connect(db_filename)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)
    
    def create_table(self, table_name):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE,
                descripcion TEXT NOT NULL,
                ultimo_precio REAL,
                cantidad INTEGER,
                moneda TEXT,
                ganancia_porcentaje REAL,
                valorizado REAL,
                simbolo TEXT,
                variacion_diaria REAL,
                ganancia REAL
            )
        ''')
        
        print(f'Table {table_name} created successfully')
        
    def commit(self):
        self.conn.commit()

    def query(self, q):
        self.create_connection()

        result = self.cursor.execute(q)

        print(result.fetchall())

    def query_all(self):
        self.create_connection()

        result = self.cursor.execute('SELECT * FROM registros')

        print(result.fetchall())
        
    def _generate_timestamp(self):
        '''Gets current date and time'''
        current_datetime = datetime.now()

        format = '%Y-%m-%d_%I-%M-%S_%p'.lower()
        filename = current_datetime.strftime(format)

        return filename
    
    def _get_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def current_datetime(self):
        current_datetime = datetime.now()
        time_now = current_datetime.astimezone(
         pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%I:%M %p')

        return f'[{time_now}]'

    def query_month(self, month=None, draw=False):
        '''Format: Y-mm'''
        self.create_connection()

        if month is None:
            month = datetime.now().strftime('%Y-%m')

        query = 'SELECT SUM(cantidad) FROM registros WHERE strftime("%Y-%m", fecha) = ?'
        result = self.cursor.execute(query, (month, ))

        sumatoria = result.fetchone()[0]
        print(f'El total de trabajos del mes {month} es: {sumatoria}')

        query = 'SELECT * FROM registros WHERE strftime("%Y-%m", fecha) = ? ORDER BY fecha DESC, id DESC'
        result = self.cursor.execute(query, (month, ))
        registros = result.fetchall()

        if draw:
            self.draw_table(registros)

        return registros

    def add_dict_data(self, data, show=True):
        for i, record in enumerate(data):
            self.add_data(
                self._get_date(), record['descripcion'], record['ultimo_precio'],
                record['cantidad'], record['moneda'],
                record['ganancia_porcentaje'], record['valorizado'],
                record['simbolo'], record['variacion_diaria'],
                record['ganancia'], False
            )
            
        if len(data) > 1:
            print(f'{self.current_datetime()} Saved {len(data)} records')
        else:
            print(f'{self.current_datetime()} Saved {len(data)} record')

    def add_data(self, date: str, descripcion: str, ultimo_precio: float,
                 cantidad: int, moneda: str, ganancia_porcentaje: float,
                 valorizado: float, simbolo: str, variacion_diaria: float,
                 ganancia: float, show=True):
        self.create_connection()

        try:
            self.cursor.execute('''
                INSERT INTO registros (fecha, descripcion, ultimo_precio,
                cantidad, moneda, ganancia_porcentaje, valorizado,
                simbolo, variacion_diaria, ganancia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (date, descripcion, ultimo_precio, cantidad, moneda,
                 ganancia_porcentaje, valorizado, simbolo,
                 variacion_diaria, ganancia)
            )

            self.commit()

        except Exception as e:
            print(str(e))

        finally:
            if show:
                print(f'{self.current_datetime()} Record saved')

    def edit_date(self, id_number, new_date):
        self.create_connection()

        self.cursor.execute('UPDATE registros SET fecha = ? WHERE id = ?',
                          (new_date, id_number))

        self.commit()

    def edit_quantity(self, id_number, new_quantity):
        self.create_connection()

        self.cursor.execute('UPDATE registros SET cantidad = ? WHERE id = ?',
                          (new_quantity, id_number))

        self.commit()

    def edit(self, id_number, new_date, new_quantity):
        self.cursor.execute(
         'UPDATE registros SET fecha = ?, cantidad = ? WHERE id = ?',
         (new_date, new_quantity, id_number))

        self.commit()

    def delete_current_month(self):
        self.create_connection()

        current_month = datetime.now().strftime('%Y-%m')

        query = 'DELETE FROM registros WHERE strftime("%Y-%m", fecha) = ?'
        self.cursor.execute(query, (current_month, ))

        self.commit()

        current_month = datetime.now().strftime('%m')
        print(f'Se han borrado los datos del mes {current_month}')

    def delete_by_id(self, id_number):
        self.create_connection()

        try:
            if id_number == list(id_number):
                for record in id_number:
                    query = 'DELETE FROM registros WHERE id = ?'
                    self.cursor.execute(query, (record, ))

                    self.commit()

                    print(f'Deleted record with ID={record}')
        except TypeError:
            query = 'DELETE FROM registros WHERE id = ?'
            self.cursor.execute(query, (id_number, ))

            self.commit()

            print(f'Deleted record with ID={id_number}')

    def delete(self):
        os.remove(self.database_filename)

        print('Database deleted')

    def close(self):
        self.conn.close()
