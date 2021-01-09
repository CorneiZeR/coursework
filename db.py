from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, update
from sqlalchemy.sql import select
from sqlalchemy_utils import database_exists, create_database
import os

db_path = os.path.join(os.path.dirname(__file__), 'main.db')
db_url = 'sqlite:///{}'.format(db_path)

# Create engine (connection)
engine = create_engine(db_url, echo=True)

# Create database file
if not database_exists(engine.url):
    create_database(engine.url)

# Create table
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('first_name', String(20), nullable=False),
              Column('second_name', String(20), nullable=False),
              Column('login', String(20), nullable=False),
              Column('password', String(128), nullable=False),
              Column('course', Integer, nullable=False),
              Column('group', String(5), nullable=False),
              Column('access', Integer, nullable=False),
              Column('statistic_tests', String(10000), nullable=False),
              Column('statistic_lections', String(10000), nullable=False)
              )
tests = Table('tests', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(20), nullable=False),
              Column('questions', String(10000)),
              Column('answers', String(1000))
              )

# Execute "Create tables"
metadata.create_all(engine)

# Create "Insert" object of Table "Users"
ins = users.insert().values(first_name='', second_name='', login='', password='', course=0, group='', access=0,
                            statistic_tests='', statistic_lections='')

# Connect to DB
conn = engine.connect()


def registration_db(fn, sn, l, p, g):
    check = True
    s = select([users.c.login])
    result = conn.execute(s)
    for row in result:
        if l == row[0]:
            check = False
            break
    result.close()
    try:
        c = 20 - int(g[-3:-1]) + 1
    except:
        c = 0
    if check:
        conn.execute(ins, first_name=fn, second_name=sn, login=l, password=p, course=c, group=g)

    return check


def log_in_db(login, password):
    search = False
    result = conn.execute(users.select())
    for row in result:
        if login == row[3] and password == row[4]:
            search = True
            break
    result.close()
    return [search, row]


def editdata(l, np, op, id):
    check = False
    result = conn.execute(users.select())
    for row in result:
        if id == row[0]:
            if row[4] == op:
                check = True
            break
    if check:
        conn.execute(update(users).where(users.c.id == id).values(login=l, password=np))
    return check


def loaddata():
    return (conn.execute(users.select()).fetchall())


def countanswers(total):
    if len(total) > 0:
        correct, all = 0, 0
        for i in total.split("|")[:-1]:
            check = i.split("(")[1][:-1].split("/")
            correct += int(check[0])
            all += int(check[1])
        return "{}/{} ({}%)".format(correct, all, str("%.2f" % (correct * 100 / all)))
    else:
        return "Тесты не пройдены"


def counttests():
    result = conn.execute(tests.select())
    count = 0
    for row in result:
        count += 1
    return count


def countlections():
    return len(os.listdir("lections"))


def add_lecion(id: int, lection: str):
    check = True
    for row in conn.execute(select([users.c.id, users.c.statistic_lections])):
        if row[0] == id:
            if lection[:-1] in str(row[1]).split("|"):
                break
            else:
                conn.execute(update(users).where(users.c.id == id).values(statistic_lections=str(row[1]) + lection))


def add_test_result(userid: int, id: int, result: list):
    check = False
    skip = False
    test = "{}({}/{})|".format(id, result[0], result[1])
    for row in conn.execute(select([users.c.id, users.c.statistic_tests])):
        if row[0] == userid:
            for x in str(row[1]).split("|")[:-1]:
                if id == int(x[0]):
                    check = True
                    if result[0] < int(x[2]):
                        skip = True
            if not skip:
                if check:
                    new = ""
                    for grade in str(row[1]).split("|")[:-1]:
                        if id != int(grade[0]):
                            new += grade + "|"
                    conn.execute(update(users).where(users.c.id == userid).values(statistic_tests=new + test))
                else:
                    conn.execute(update(users).where(users.c.id == userid).values(statistic_tests=str(row[1]) + test))
            else:
                break


def get_tests():
    lst = []
    for row in conn.execute(tests.select()):
        lst.append(row[1])
    return lst


def get_test(name):
    lst = []
    for row in conn.execute(tests.select()):
        if row[1] == name:
            first = str(row[2]).split("|")[:-1]
            second = str(row[3]).split("|")[:-1]
            for i in range(len(second)):
                second[i] = second[i].split(".")
            lst = [first, second]
            break
    if len(lst) == 0:
        conn.execute(tests.insert().values(name="test name", questions="test question|", answers="answer1.answer2|"))
        return get_tests()
    else:
        return lst


def get_test_id_by_name(name):
    for row in conn.execute(tests.select()):
        if row[1] == name:
            return int(row[0])


def add_test(name: str, text: str):
    questions = ""
    answers = ""
    for line in text.split("\n"):
        temp = line.split("|")
        questions += temp[0] + "|"
        answers += "{}.{}|".format(temp[1], temp[2])
    conn.execute(tests.insert().values(name=name, questions=questions, answers=answers))


def delete_test_by_id(id:int):
    conn.execute(tests.delete().where(tests.c.id == id))


def search_by_second_name(second_name:str):
    for row in conn.execute(users.select()):
        if row[2] == second_name:
            return row
    return False


def get_test_name_by_id(id:int):
    for row in conn.execute(select([tests.c.id, tests.c.name])):
        if int(row[0]) == int(id):
            return row[1]