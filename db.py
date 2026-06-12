from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    port=int(os.getenv("DB_PORT")),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def save_report(
    recipient_email,
    transcript,
    summary,
    work_completed,
    issues_identified,
    safety_observations,
    next_steps
):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (
            recipient_email,
            transcript,
            summary,
            work_completed,
            issues_identified,
            safety_observations,
            next_steps
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            recipient_email,
            transcript,
            summary,
            work_completed,
            issues_identified,
            safety_observations,
            next_steps
        )
    )

    conn.commit()
    cursor.close()

def get_reports():

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               recipient_email,
               created_at,
               work_completed,
               issues_identified,
               safety_observations,
               next_steps
        FROM reports
        ORDER BY created_at DESC
    """)

    reports = cursor.fetchall()

    cursor.close()

    return reports