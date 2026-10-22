import os
from datetime import date
import psycopg2
from psycopg2.extras import Json, execute_values
from dotenv import load_dotenv
from fsa_client import get_establishments

load_dotenv()

def load(authority_id: int, run_date: date) -> int:
    rows = [(e["FHRSID"], Json(e), run_date)
            for e in get_establishments(authority_id)]

    # api returns 200 + no data for bad ID, fail here
    if not rows:
        raise ValueError(f"0 rows for authority {authority_id}; check the ID")

    conn = psycopg2.connect(
        host=os.environ.get("PG_HOST", "localhost"), dbname="fsa",
        user=os.environ["PG_USER"], password=os.environ["PG_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO raw.establishments (fhrs_id, payload, run_date)
            VALUES %s
            ON CONFLICT (fhrs_id, run_date) DO NOTHING
        """, rows)
    conn.close()
    return len(rows)

if __name__ == "__main__":
    n = load(int(os.environ["FSA_AUTHORITY_ID"]), date.today())
    print(f"Loaded {n} establishments")
    