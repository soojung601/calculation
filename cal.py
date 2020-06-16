import sqlite3

conn = sqlite3.connect('/Users/soochungsohn/Documents/calculation/templates/cal.db',
                       isolation_level=None, check_same_thread=False)

cursor = conn.cursor()


def make_table():
    create_text = f"CREATE TABLE IF NOT EXISTS CAL(id_num INTEGER PRIMARY KEY, inputnum integer, status text)"
    cursor.execute(create_text)


def get_num(first_num, text):
    cursor.execute(
        f"INSERT INTO CAL('inputnum', 'status') VALUES({first_num}, '{text}')")


def reset_table():
    cursor.execute("delete from CAL")


def get_result(last_num):
    cursor.execute(
        f"insert into CAL('inputnum', 'status') VALUES({last_num}, NULL)")
    cursor.execute("select id_num,status from CAL where status = 'multi'")
    first_cal = cursor.fetchall()
    cursor.execute("select id_num,status from CAL where status = 'divide'")
    first_cal += cursor.fetchall()
    first_cal_sorted = sorted(first_cal, key=lambda first_cal: first_cal[0])
    for i in first_cal_sorted:
        if i[1] == 'multi':
            cursor.execute(
                f"select inputnum from CAL where id_num = {i[0]} OR id_num = {i[0]+1}")
            cal_nums = cursor.fetchall()
            cursor.execute(f"delete from CAL where id_num = {i[0]}")
            cursor.execute(
                f"UPDATE CAL set inputnum = {cal_nums[0][0] * cal_nums[1][0]} where id_num = {i[0]+1}")
        else:
            cursor.execute(
                f"select inputnum from CAL where id_num = {i[0]} OR id_num = {i[0]+1}")
            cal_nums = cursor.fetchall()
            cursor.execute(f"delete from CAL where id_num = {i[0]}")
            cursor.execute(
                f"UPDATE CAL set inputnum = {cal_nums[0][0] / cal_nums[1][0]} where id_num = {i[0]+1}")
    cursor.execute("select inputnum, status from CAL")
    end_cal = cursor.fetchall()
    i = 0
    result_num = end_cal[0][0]
    while i < len(end_cal):
        if end_cal[i][1] == 'add':
            result_num += end_cal[i+1][0]
        elif end_cal[i][1] == 'minus':
            result_num -= end_cal[i+1][0]
        else:
            cursor.execute(
                f"INSERT into CAL('inputnum','status') VALUES({result_num},'result')")
        i += 1
    cursor.execute("select inputnum from CAL where status ='result'")
    end_result = cursor.fetchall()[0]
    return end_result[0]

