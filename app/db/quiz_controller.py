import aiosqlite

from app.core.config import SQLITE_DB_FILE


async def create_table():
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY,
            question_index INTEGER,
            correct_answers
            )"""
        )
        await db.commit()


async def update_quiz_index(user_id, index, correct_answers):
    """
    Обновляем запись для заданного пользователя
    """
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO quiz_state (user_id, question_index, correct_answers) VALUES (?, ?, ?)",
            (user_id, index, correct_answers),
        )
        await db.commit()


async def get_quiz_index(user_id):
    """
    Получаем запись для заданного пользователя
    """
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        async with db.execute(
            "SELECT question_index, correct_answers FROM quiz_state WHERE user_id = (?)",
            (user_id,),
        ) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results
            else:
                return 0, 0
