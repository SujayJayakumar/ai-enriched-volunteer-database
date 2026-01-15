import argparse
import sqlite3
from pathlib import Path


DB_PATH = Path("data/volunteer_data.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def show_mentors(limit, warn_uncertain=False):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            m.name,
            p.persona,
            p.confidence,
            m.last_active,
            GROUP_CONCAT(s.skill_name, ', ') AS skills
        FROM members m
        JOIN persona_analysis p
            ON m.member_id = p.member_id
        LEFT JOIN member_skills ms
            ON m.member_id = ms.member_id
        LEFT JOIN skills s
            ON ms.skill_id = s.skill_id
        WHERE p.persona IN ('Mentor Material', 'Uncertain')
        GROUP BY m.member_id
        ORDER BY
            p.confidence DESC,
            m.last_active DESC
        LIMIT ?
        """,
        (limit,),
    )


    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No mentors found.")
        return

    print("\nTop Potential Mentors:\n")
    for i, (name, persona, confidence, last_active, skills) in enumerate(rows, start=1):
        print(f"{i}. {name}")
        print(f"   Persona: {persona}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Last Active: {last_active}")
        print(f"   Skills: {skills}")

        if warn_uncertain and persona == "Uncertain":
            print("   ⚠️  Warning: Low-confidence AI classification. Human review recommended.")

        print("-" * 40)



def main():
    parser = argparse.ArgumentParser(description="Volunteer OS CLI")
    parser.add_argument(
        "--mentors",
        action="store_true",
        help="Show ranked potential mentors",
    )
    parser.add_argument(
        "--warn-uncertain",
        action="store_true",
        help="Show warning for low-confidence (Uncertain) personas",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of results to show",
    )

    args = parser.parse_args()

    if args.mentors:
        show_mentors(args.limit, warn_uncertain=args.warn_uncertain)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
