from fastapi import FastAPI
import sqlite3

m = FastAPI()

con = sqlite3.connect("db.db")

c = con.cursor()

c.execute("""
create table if not exists user (
    id integer not null,
    fullname text not null,
    primary key(id)
)
""")

info = c.execute("""
select * from user
""").fetchall()

print(info)


@m.get("/")
def _():
    data = """

    Usage:
        run :
            uvicorn main:m --reload
        localhost:8000 or 8080 ports

        /firstname lastname 
            for adding your info to db or checking info into db.

    """

    return info


@m.get("/users")
def _():
    con = sqlite3.connect("db.db")
    c = con.cursor()
    data = c.execute("""
    select * from user
    """).fetchall()

    return data


@m.get("/{fullname}")
def _(fullname):
    user = f"{fullname}",

    con = sqlite3.connect("db.db")
    c = con.cursor()


    print(user[0])

    # data = c.execute(f"""
    # select fullname from user where fullname like {user}
    # """).fetchone()
    #
    # print(data)


    try:

        data = c.execute(f"""
        SELECT fullname FROM user WHERE fullname = '{user[0]}' LIMIT 1;
        """).fetchone()[0]

        print(data)

        if fullname == data:
            return "Sorry, your info already into db!"


        else:
            return "Sorry, Some error happened or your info already into db!"

        con.close()

    except Exception as err:

        if err:
            c.execute("""
            insert into user(fullname) values(?)
            """, user)
            con.commit()
            return f"Hi, bro! Your info added to db!"
    return f"{user}"






con.close()