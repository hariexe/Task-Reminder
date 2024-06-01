import sqlite3

class Database:
    def __init__(self, db_path='task_reminder.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        #-- 0: rendah, 1: sedang, 2: tinggi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                task_datetime TEXT NOT NULL,
                note TEXT,
                priority INTEGER DEFAULT 0,  
                category INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history_table (
                task_name TEXT NOT NULL,
                task_datetime TEXT NOT NULL,
                note TEXT,
                priority INTEGER DEFAULT 0,  
                category INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def commit_changes(self):
        self.conn.commit()

    def register_user(self, nickname, password, email):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (nickname, password, email) VALUES (?, ?, ?)',
                        (nickname, password, email))
        self.conn.commit()

    def authenticate_user(self, nickname, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE nickname = ? AND password = ?', 
                       (nickname, password))
        return cursor.fetchone() is not None
    
    def add_personal_task(self, task_name, task_datetime, priority, category):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO personal_tasks (task_name, task_datetime, priority, category) VALUES (?, ?, ?, ?)', 
                       (task_name, task_datetime, priority, category))
        self.commit_changes()  # Panggil commit_changes setelah perubahan

    def get_personal_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT task_name FROM personal_tasks ORDER BY priority DESC, task_datetime')
        tasks = [item[0] for item in cursor.fetchall()]
        return tasks
    
    def get_task_details(self, task_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT task_name, task_datetime FROM personal_tasks WHERE task_name = ?', 
                       (task_name,))
        task_details = cursor.fetchone()
        return task_details
    
    def set_task_note(self, task_name, note):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE personal_tasks SET note = ? WHERE task_name = ?', 
                       (note, task_name))
        self.commit_changes()
    
    def get_task_note(self, task_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT note FROM personal_tasks WHERE task_name = ?',
                        (task_name,))
        note = cursor.fetchone()
        return note[0] if note else ""
    
    def set_task_priority(self, task_name, priority):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE personal_tasks SET priority = ? WHERE task_name = ?',
                        (priority, task_name))
        self.commit_changes()

    def get_task_priority(self, task_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT priority FROM personal_tasks WHERE task_name = ?',
                        (task_name,))
        priority = cursor.fetchone()
        return priority[0] if priority else "Low"  # Default: rendah
    
    def set_task_category(self, task_name, category):
        # Implementasi logika untuk menyimpan kategori ke database
        cursor = self.conn.cursor()
        cursor.execute("UPDATE personal_tasks SET category = ? WHERE task_name = ?", 
                       (category, task_name))
        self.commit_changes()

    def get_task_category(self, task_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT category FROM personal_tasks WHERE task_name = ?',
                        (task_name,))
        category = cursor.fetchone()
        return category[0] if category else "Work"  # Default: work

    def move_to_history_table(self, task_name, task_datetime, note, priority, category):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO history_table (task_name, task_datetime, note, priority, category) VALUES (?, ?, ?, ?, ?)', 
                    (task_name, task_datetime, note, priority, category))
        self.commit_changes()

    def get_completed_personal_tasks(self):
        cursor = self.conn.cursor()
        # Select all columns from history_table
        cursor.execute('SELECT * FROM history_table')
        completed_tasks = cursor.fetchall()
        return completed_tasks
    
    def remove_personal_task(self, task_name):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM personal_tasks WHERE task_name = ?', 
                       (task_name,))
        self.commit_changes()  # Panggil commit_changes setelah perubahan

    def reset_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM history_table')  # Adjust this query based on your database schema
        self.commit_changes()