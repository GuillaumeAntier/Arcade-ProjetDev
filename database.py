import sqlite3

class Database :
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.conn.commit()
        
    def save_settings(self, settings_dict) :
        return
    
    def load_settings(self) :
        return
    
    def save_score(self, player_name, score) :
        self.cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
        
    def get_top_scores(self, limit = 10) :
        return