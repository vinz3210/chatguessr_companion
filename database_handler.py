import os
import sqlite3
import time

class DatabaseHandler:
    def __init__(self, global_settings):
        self.global_settings = global_settings
        self.file = global_settings.get_db_path()
        if(os.path.exists(self.file) == False):
            print("Database file not found")
            return
        self.db = sqlite3.connect(self.file)
        self.guessers = []
        self.start_time = time.time()
    
    def get_streamer_name(self):
        try:
            query = "select * from Users WHERE id = 'BROADCASTER';"
            cursor = self.db.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results[0][1]
        except:
            return None
        
    def _sum_up_stats(self, results):
        out_results = {}
        for username in results:
            if username[0] == self.global_settings.get_streamer_name():
                continue
            if username[0] not in out_results.keys():
                out_results[username[0]] = 0
            out_results[username[0]] += 1
        #sort out_results by value
        out_results = dict(sorted(out_results.items(), key=lambda item: item[1], reverse=True))
        return out_results
    
    def getStatsLast30Days(self):
        # query
        query = "SELECT username from game_winners JOIN users on game_winners.user_id = users.id WHERE game_winners.created_at > unixepoch('now', '-30 days')"
        # execute the query
        cursor = self.db.cursor()
        cursor.execute(query)
        # fetch the results
        results = cursor.fetchall()
        # close the cursor
        cursor.close()
        return self._sum_up_stats(results)
    
    def getTotalStats(self):
        # query
        query = "SELECT username from game_winners JOIN users on game_winners.user_id = users.id"
        # execute the query
        cursor = self.db.cursor()
        cursor.execute(query)
        # fetch the results
        results = cursor.fetchall()
        # close the cursor
        cursor.close()
        return self._sum_up_stats(results)
    
    def get_current_game_state(self):
        # query
        query = "SELECT state from games order by created_at DESC limit 1;"
        # execute the query
        cursor = self.db.cursor()
        cursor.execute(query)
        # fetch the results
        results = cursor.fetchall()
        cursor.close()
        return results[0][0]=="started"

    def getNewUsers(self, start_time):
        #query
        query = f"SELECT DISTINCT users.username from users join guesses on users.id = guesses.user_id where guesses.created_at > {start_time} order by guesses.created_at DESC;"
        # execute the query
        cursor = self.db.cursor()
        cursor.execute(query)
        # fetch the results
        results = cursor.fetchall()
        cursor.close()

        for result in results:
            if result[0] not in self.guessers:
                self.guessers.append(result[0])
        return self.guessers