from sqlite3 import connect


"""
This script is used to get the PID of the current process.
It is used by the stop.py script to stop the current process.

The script will create a database called "database.sqlite" in ./lib and a table called "pids" in that database.
The table will have one column called "pid" which will contain the PID of the process.

If the table is empty, the script will return None.

If the table is not empty, the script will return the first PID in the table and will delete it from the table.
"""


def get_pid() -> int | None:
    """Return the PID of the current process."""
    with connect("./db/database.sqlite") as con:
        with open("./db/build.sql", "r") as f:
            con.executescript(f.read())
        con.commit()

        cur = con.cursor()

        if pid := cur.execute("SELECT pid FROM pids LIMIT 1").fetchone():
            pid = pid[0]
            cur.execute("DELETE FROM pids WHERE pid = ?", (pid,))
            con.commit()
        return pid


if __name__ == "__main__":
    print(get_pid())
