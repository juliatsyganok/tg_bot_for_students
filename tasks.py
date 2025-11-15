import datetime

TASKS = {
    "2024-12-01": {
        "task_text": "🔢 Задание на 1 декабря: Сколько будет 5 + 3? Пришлите только число.",
        "correct_answer": "8",
        "max_score": 1
    }
}

def get_todays_task():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return TASKS.get(today)

def check_answer(task_date, user_answer):
    task = TASKS.get(task_date)
    if not task:
        return False, 0
    
    user_answer_clean = user_answer.strip().lower()
    correct_answer_clean = task["correct_answer"].strip().lower()
    
    is_correct = user_answer_clean == correct_answer_clean
    
    if is_correct:
        return True, task["max_score"]
    else:
        return False, 0

def get_task_by_date(date_str):
    return TASKS.get(date_str)