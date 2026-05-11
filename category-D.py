import csv
import sqlite3
import re

CSV_FILE = "student_scores.csv"
TXT_FILE = "student_comments.txt"
DB_FILE = "elt_student_data.db"


def extract_structured_data():
    records = []

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records


def extract_unstructured_data():
    records = []

    with open(TXT_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(line)

    return records


def connect_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    return conn, cursor


def create_raw_tables(cursor):
    """
    TODO #1: CREATE TABLE

    Create two raw tables.

    Table 1: raw_student_scores

    Columns:
    id INTEGER PRIMARY KEY AUTOINCREMENT
    student_id TEXT
    name TEXT
    course TEXT
    quiz TEXT
    exam TEXT
    attendance TEXT

    Table 2: raw_student_comments

    Columns:
    id INTEGER PRIMARY KEY AUTOINCREMENT
    raw_text TEXT
    """

    # Write CREATE TABLE code here
    pass


def insert_structured_records(cursor, records):
    """
    TODO #2A: INSERT INTO

    Insert CSV data into raw_student_scores.

    Fields:
    student_id
    name
    course
    quiz
    exam
    attendance
    """

    # Write INSERT INTO code here
    pass


def insert_unstructured_records(cursor, records):
    """
    TODO #2B: INSERT INTO

    Insert TXT raw lines into raw_student_comments.

    Field:
    raw_text
    """

    # Write INSERT INTO code here
    pass


def transform_data_inside_database(cursor):
    cursor.execute("DROP TABLE IF EXISTS transformed_student_scores")
    cursor.execute("DROP TABLE IF EXISTS transformed_student_comments")
    cursor.execute("DROP TABLE IF EXISTS final_student_report")

    cursor.execute("""
        CREATE TABLE transformed_student_scores AS
        SELECT
            CAST(student_id AS INTEGER) AS student_id,
            name,
            course,
            CAST(quiz AS INTEGER) AS quiz,
            CAST(exam AS INTEGER) AS exam,
            CAST(attendance AS INTEGER) AS attendance,
            ROUND(
                (CAST(quiz AS REAL) * 0.30) +
                (CAST(exam AS REAL) * 0.50) +
                (CAST(attendance AS REAL) * 0.20),
                2
            ) AS final_grade,
            CASE
                WHEN ROUND(
                    (CAST(quiz AS REAL) * 0.30) +
                    (CAST(exam AS REAL) * 0.50) +
                    (CAST(attendance AS REAL) * 0.20),
                    2
                ) >= 75 THEN 'Passed'
                ELSE 'Failed'
            END AS status
        FROM raw_student_scores
    """)

    cursor.execute("""
        CREATE TABLE transformed_student_comments AS
        SELECT
            CAST(
                SUBSTR(
                    raw_text,
                    INSTR(raw_text, 'Student ID: ') + LENGTH('Student ID: '),
                    INSTR(raw_text, ' |') - (INSTR(raw_text, 'Student ID: ') + LENGTH('Student ID: '))
                ) AS INTEGER
            ) AS student_id,
            TRIM(
                SUBSTR(
                    raw_text,
                    INSTR(raw_text, 'Comment: ') + LENGTH('Comment: ')
                )
            ) AS comment
        FROM raw_student_comments
    """)

    cursor.execute("""
        CREATE TABLE final_student_report AS
        SELECT
            s.student_id,
            s.name,
            s.course,
            s.quiz,
            s.exam,
            s.attendance,
            s.final_grade,
            s.status,
            c.comment
        FROM transformed_student_scores s
        LEFT JOIN transformed_student_comments c
        ON s.student_id = c.student_id
    """)


def select_final_report(cursor):
    """
    TODO #3: SELECT FROM

    Select and display all records from final_student_report.

    Expected columns:
    student_id, name, course, quiz, exam, attendance,
    final_grade, status, comment
    """

    # Write SELECT code here
    pass


def main():
    structured_records = extract_structured_data()
    unstructured_records = extract_unstructured_data()

    conn, cursor = connect_database()

    create_raw_tables(cursor)

    cursor.execute("DELETE FROM raw_student_scores")
    cursor.execute("DELETE FROM raw_student_comments")

    insert_structured_records(cursor, structured_records)
    insert_unstructured_records(cursor, unstructured_records)

    transform_data_inside_database(cursor)

    conn.commit()

    select_final_report(cursor)

    conn.close()


if __name__ == "__main__":
    main()