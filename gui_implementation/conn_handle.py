import psycopg2
import config
from tkinter import messagebox as msg

class DBConnection:
    connection = None
    def __new__(classe):
        if classe.connection is None:
            classe.connection = super().__new__(classe)
        return classe.connection

    def _connect(self):
        try:
            return psycopg2.connect(
                host=config.host,
                database=config.name,
                user=config.user,
                password=config.password
            )
        except Exception as e:
            raise ConnectionError(f"Falha na conxão: {e}")

    def execute(self, query, params=None, fetch=False):
        conn = None
        try:
            conn = self._connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                        
                if fetch:
                    return cursor.fetchall()
            
                conn.commit()
                msg.showinfo(message="Operação bem sucedida!")
        
        except Exception as e:
            if conn:
                print(e)
                msg.showerror(message="Erro de Comando: Input Inválido")
                conn.rollback()
            raise RuntimeError(f"Query falhou: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    db = DBConnection()

