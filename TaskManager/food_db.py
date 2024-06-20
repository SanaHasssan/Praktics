import sqlite3

class FoodDB:
    def __init__(self):
        self.database_connection = sqlite3.connect("food.db")
        self.create_table()

    def create_table(self):
        cursor = self.database_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS food (name TEXT, items TEXT, amount REAL)")
        self.database_connection.commit()

    def get_foods(self):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT name FROM food")
        foods = cursor.fetchall()
        return [food[0] for food in foods]

    def save_food(self, food_name):
        print(food_name)
        cursor = self.database_connection.cursor()
        cursor.execute("INSERT INTO food (name) VALUES (?)", (food_name,))
        self.database_connection.commit()

    def delete_food(self, food_name):
        cursor = self.database_connection.cursor()
        cursor.execute("DELETE FROM food WHERE name=?", (food_name,))
        self.database_connection.commit()
