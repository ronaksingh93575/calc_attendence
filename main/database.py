import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect("attendance.db")
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS subjects(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            month TEXT,

            subject_name TEXT,

            classes_per_five INTEGER

        )

        """)

        self.conn.commit()

    def clear_month(self, month):

        self.cursor.execute(
            "DELETE FROM subjects WHERE month=?",
            (month,)
        )

        self.conn.commit()

    def save_subject(
            self,
            month,
            subject,
            classes
    ):

        self.cursor.execute(

            """

            INSERT INTO subjects
            (
                month,
                subject_name,
                classes_per_five
            )

            VALUES
            (
                ?,
                ?,
                ?
            )

            """,

            (
                month,
                subject,
                classes
            )

        )

        self.conn.commit()

    def get_subjects(self, month):

        self.cursor.execute(

            """

            SELECT
            subject_name,
            classes_per_five

            FROM subjects

            WHERE month=?

            """,

            (month,)

        )

        return self.cursor.fetchall()