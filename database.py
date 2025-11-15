import sqlite3
import datetime


def init_database():
    """Создаем таблицы в базе данных"""
    conn = sqlite3.connect('school_bot.db')
    cursor = conn.cursor()
    
 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,    -- Уникальный ID из Telegram
            username TEXT,                  -- @username ученика
            first_name TEXT,                -- Имя ученика
            date_joined DATETIME DEFAULT CURRENT_TIMESTAMP  -- Когда зарегистрировался
        )
    ''')
    
    # Таблица баллов - храним ответы и набранные баллы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
            user_id INTEGER,                -- ID ученика
            task_date TEXT,                 -- Дата задания (например "2024-12-01")
            score INTEGER DEFAULT 0,        -- Сколько баллов получил
            answer TEXT,                    -- Ответ ученика
            PRIMARY KEY (user_id, task_date) -- Уникальная пара: ученик+дата
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    """Добавляем нового пользователя в базу"""
    conn = sqlite3.connect('school_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    ''', (user_id, username, first_name))
    
    conn.commit()
    conn.close()

def save_answer(user_id, task_date, answer, score):
    conn = sqlite3.connect('school_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO user_scores (user_id, task_date, answer, score)
        VALUES (?, ?, ?, ?)
    ''', (user_id, task_date, answer, score))
    
    conn.commit()
    conn.close()

def get_user_score(user_id):
    """Получаем общее количество баллов пользователя"""
    conn = sqlite3.connect('school_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT SUM(score) as total_score FROM user_scores 
        WHERE user_id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result[0] is not None else 0

def get_all_users():
    """Получаем список всех пользователей для рассылки"""
    conn = sqlite3.connect('school_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return users