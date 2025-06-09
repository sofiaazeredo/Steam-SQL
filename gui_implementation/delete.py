from conn_handle import DBConnection

class Delete(DBConnection):
    # Example: object.delete("clientes", "id = %s", (5,))
    def delete(self, table: str, condition: str, params):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute(query,params)
                
