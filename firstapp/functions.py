import psycopg2
import json

def get_users():
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if len(users) == 0:
        print("There is no any users")
    else:
        print(users)

    if conn:
        conn.commit()
        cursor.close()
        conn.close()
    return users

def set_user(uname, upassword):
    insert_query = "INSERT INTO users(user_name, user_pass) VALUES ('{}', '{}')".format(uname, upassword)

    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()
    cursor.execute(insert_query)

    if (conn):
        conn.commit()
        cursor.close()
        conn.close()

    return True


def get_orders(user):
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    get_id_query = "SELECT user_id FROM users WHERE user_name = '%s'" % user
    cursor.execute(get_id_query)
    uid = cursor.fetchone()

    select_query = "SELECT myorder FROM orders WHERE user_id = %s" % uid[0]
    cursor.execute(select_query)
    orders = cursor.fetchall()

    if len(orders) == 0:
        print("There is no any orders")
    else:
        for o in orders:
            print(o)

    if conn:
        conn.commit()
        cursor.close()
        conn.close()

    return orders


def set_order(user, order):
    select_user_query = "select user_id from users where user_name = '{}'".format(user)

    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()
    cursor.execute(select_user_query)
    uid = cursor.fetchone()
    insert_query = "INSERT INTO orders(myorder, user_id) VALUES ('{}', {})".format(order, uid[0])
    cursor.execute(insert_query)

    if conn:
        conn.commit()
        cursor.close()
        conn.close()

    return True


def get_cinemas():
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    get_query = "SELECT * FROM cinemas"
    cursor.execute(get_query)
    cins = cursor.fetchall()

    if conn:
        conn.commit()
        cursor.close()
        conn.close()
    return cins


def get_films():
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    get_query = "SELECT * FROM movies"
    cursor.execute(get_query)
    films = cursor.fetchall()

    if conn:
        conn.commit()
        cursor.close()
        conn.close()
    return films


def get_seats(sch_id):
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    get_query = "SELECT * FROM seats WHERE sch_id = {} order by s_num".format(sch_id)
    cursor.execute(get_query)
    seats = cursor.fetchall()

    if conn:
        conn.commit()
        cursor.close()
        conn.close()
    return seats


def bubble_sort(list): #list of dictionaries of schedule
    length = len(list) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if list[i]['time'] > list[i+1]['time']:
                sorted = False
                list[i], list[i+1] = list[i+1], list[i]
    return list


def get_film_info(fid, cid):
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    # Setting the film's information
    film_query = "SELECT * FROM movies WHERE m_id = {}".format(fid)
    cursor.execute(film_query)
    film = cursor.fetchone()
    film = [film[0], film[1], film[2]]
#    film[0] - id
#    film[1] - name
#    film[2] - description

    # Setting the film's schedule
    hall_query = "SELECT ch_id FROM cin_hall WHERE c_id = {}".format(cid)
    cursor.execute(hall_query)
    hids = cursor.fetchall()
    print(hids)

    get_query = "SELECT * FROM schedule WHERE m_id = {} AND (ch_id = {} OR ch_id = {} OR ch_id = {})"\
                .format(fid, hids[0][0], hids[1][0], hids[2][0])
    cursor.execute(get_query)
    sched = cursor.fetchall()
    print(sched)


    schedule = []
    for s in sched:
        get_query = "SELECT * FROM price as p, schedule as s WHERE s.sch_id = {} AND s.sch_time = p.time_id".format(s[0])
        cursor.execute(get_query)
        price = cursor.fetchone()
        schedule.append({'id': s[0], 'time': s[1], 'hall' : s[3],
                         'kids': price[1], 'students': price[2], 'adults': price[3]})

    f_info = []
    f_info.extend(film)
    f_info.append(schedule)
    print(f_info)
    return f_info

def book_seats(user, film_id, cinema, seats, tickets):


    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="postgres")
    cursor = conn.cursor()

    # Selecting all info of our bseats
    bseats = []
    for s in seats:
        select_seat_query = "select * from seats where s_id = {}".format(s)
        cursor.execute(select_seat_query)
        seat = cursor.fetchone()
        bseats.append(seat)

    for s in bseats:
        update_query = "UPDATE seats SET status = {} WHERE s_id = {}".format(True, s[0])
        cursor.execute(update_query)

    # Finding schedule of our film
    film_info = get_film_info(film_id, cinema[0])
    sched = film_info[3]
    v = 0
    for s in range(0, len(sched)):
        if bseats[0][3] == sched[s]["id"]:
            v = s
            break

    # Making total cost
    cost = tickets["kids"]*sched[v]["kids"] + tickets["students"]*sched[v]["students"] + tickets["adults"]*sched[v]["adults"]

    # Making an order
    order_di = {
        "cinema" : cinema[1],
        "film" : film_info[1],
        "time" : sched[v]["time"],
        "hall" : sched[v]["hall"],
        "seats" : [i[1] for i in bseats],
        "tickets" : tickets,
        "totalCost": cost
    }
    print(order_di)
    set_order(user, json.dumps(order_di))

    if conn:
        conn.commit()
        cursor.close()
        conn.close()

    return