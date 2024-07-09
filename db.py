import sqlite3


class DbHandler():

    def __init__(self, **kwargs):
        super().__init__()
        self.__kwargs = kwargs
        self.__db_name = 'cars.db'
        self.__connection = self.__db_connect()

    def __db_connect(self):
        con = sqlite3.connect(self.__db_name, **self.__kwargs)
        con.autocommit = False
        return con

    def execute_query(self, query: str):
        self.__connection.execute('%s' % query)
        self.close_connection()

    def close_connection(self):
        self.__connection.close()


db = DbHandler()

# db.execute_query('''
# CREATE TABLE cars (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     register_number VARCHAR(255) NOT NULL,
#     voivodeship VARCHAR(255) NOT NULL,
#     brand VARCHAR(255) NOT NULL,
#     model VARCHAR(255) NOT NULL,
#     color VARCHAR(255) NOT NULL,
#     city VARCHAR(255) NOT NULL,
#     photo BLOB
# );
# ''')

# db.execute_query('''
# INSERT INTO cars (register_number, voivodeship, brand, model, color, city, photo)
# VALUES
# ('DQRS7890', 'Wielkopolskie', 'Audi', 'A4', 'White', 'Poznań', NULL);
# ''')
