import sqlite3
import logging as log_tg
import colorama
from colorama import Fore

NAME_BASE = "database.db"

colorama.init()

log_tg.basicConfig(format="[%(asctime)s] %(levelname)s \t | \t%(message)s", datefmt='%H:%M:%S', level=1)
log_tg.addLevelName(3, Fore.BLUE + "SQL\t")

def return_table(table: str) -> list: 
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT * FROM {table}"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    log_tg.log(3, msg=f"Возращаем таблицу {table}{Fore.RESET}")
    return results

def check(table: str, columns: str, search_text, log=1) -> list: 
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT * FROM {table} WHERE {columns} = '{search_text}';"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    if log == 1:
        log_tg.log(
            3,
            msg=f"Возращаем из таблицы {table}, строчку с поисковыми значениями: {columns} -> {search_text}{Fore.RESET}",
        )
    return list(results)

def check_contains(table: str, columns: str, search_text: str) -> list: 
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT *\nFROM {table}\nWHERE ',' || {columns} || ',' LIKE '%{search_text}%';"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    log_tg.log(
        3,
        msg=f"Возращаем из таблицы {table}, строчку с поисковыми значениями содержащими: {columns} -> {search_text}{Fore.RESET}",
    )
    return list(results)

def insert(table: str, columns, values) -> None:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""INSERT INTO {table} ({columns})
                    VALUES ({values});"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(3, msg=f"Вставляем новую строчку в таблицу....{Fore.RESET}")
    log_tg.log(3, msg=" ".join(columns.split(",")) + Fore.RESET)
    log_tg.log(3, msg=" ".join(values.split(",")) + Fore.RESET)

def count_row(table: str) -> int:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT * FROM {table}"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    log_tg.log(3, msg=f"Возращаем количество строк в таблице: {table}{Fore.RESET}")
    return len(results)

def set_state(id: int, state) -> None:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""UPDATE users
                    SET state = {state}
                    WHERE user_id = '{id}';"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(
        3, msg=f"Установили статус '{state}' для пользователя {id}{Fore.RESET}"
    )
    return

def delete_chat(id: int) -> None:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""DELETE FROM "main"."chats" WHERE Unique_ID = '{id}'"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(
        3,
        msg=f"Удалили строчку из таблицы 'chats' с значением 'chat_id' -> {id}{Fore.RESET}",
    )
    return

def remove_line(table, column, value):
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""DELETE FROM {table} WHERE {column} = '{value}'"""
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(
        3,
        msg=f"Удалили строчку из таблицы '{table}' с значением '{column}' -> {value}{Fore.RESET}",
    )
    return

def get_pos_line(table: str, pos: int) -> int:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT * FROM {table} LIMIT 1 OFFSET {pos};"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    log_tg.log(
        3,
        msg=f"Получаем cуществует ли строчка из таблицы '{table}' с индексом {pos}{Fore.RESET}",
    )
    return len(results)

def get_pos_line_result(table: str, pos: int) -> list:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""SELECT * FROM {table} LIMIT 1 OFFSET {pos};"""
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    log_tg.log(
        3,
        msg=f"Получаем строчку из таблицы '{table}' с индексом {pos}{Fore.RESET}",
    )
    return results

def set(table: str, search_column: str, search_value, change_column: str, change_value) -> None:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""UPDATE {table} SET {change_column} = "{change_value}" WHERE {search_column} = "{search_value}" """
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(
        3,
        msg=f"Задаем '{change_column}' -> '{change_value}' в таблице '{table}', используя поисковой запрос: {search_column} -> {search_value}{Fore.RESET}",
    )
    return


def set_null(table: str, search_column: str, search_value, change_column) -> None:
    conn = sqlite3.connect(NAME_BASE)
    cursor = conn.cursor()
    sql_query = f"""UPDATE {table} SET {change_column} = NULL WHERE {search_column} = "{search_value}" """
    cursor.execute(sql_query)
    conn.commit()
    conn.close()
    log_tg.log(
        3,
        msg=f"Задаем 0-ое значение для столбика '{change_column}', используя поисковой запрос: {search_column} -> {search_value}{Fore.RESET}",
    )
    return