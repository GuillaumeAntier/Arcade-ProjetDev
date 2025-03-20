import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def create_table(self, table_name, columns):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.conn.commit()
    
    def save_settings(self, settings_dict):
        """
        Save player settings to the database
        settings_dict format: {"player_id": id, "setting_name": value, ...}
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player_settings (player_id TEXT, setting_name TEXT, value REAL, PRIMARY KEY (player_id, setting_name))")
        
        for player_id, settings in settings_dict.items():
            for setting_name, value in settings.items():
                self.cursor.execute(
                    "INSERT OR REPLACE INTO player_settings (player_id, setting_name, value) VALUES (?, ?, ?)",
                    (player_id, setting_name, value)
                )
        
        self.conn.commit()
    
    def load_settings(self, player_id=None):
        """
        Load player settings from the database
        If player_id is None, load all settings
        Returns a dictionary of settings
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player_settings (player_id TEXT, setting_name TEXT, value REAL, PRIMARY KEY (player_id, setting_name))")
        
        if player_id:
            self.cursor.execute("SELECT setting_name, value FROM player_settings WHERE player_id = ?", (player_id,))
            rows = self.cursor.fetchall()
            return {row[0]: row[1] for row in rows}
        else:
            self.cursor.execute("SELECT player_id, setting_name, value FROM player_settings")
            rows = self.cursor.fetchall()
            
            settings = {}
            for row in rows:
                player_id, setting_name, value = row
                if player_id not in settings:
                    settings[player_id] = {}
                settings[player_id][setting_name] = value
            
            return settings
    
    def save_score(self, player_name, score):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, player_name TEXT, score INTEGER)")
        self.cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
        self.conn.commit()
        
    def get_top_scores(self, limit=10):
        self.cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()