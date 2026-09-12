import json

from src.database.postgres import get_connection


def insert_papers():

    with open("data/research_papers.json", "r", encoding="utf-8") as file:
        papers = json.load(file)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO research_papers (
            schema_version,
            record_type,
            title,
            authors,
            paper_url,
            github_url,
            github_stars,
            published_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (paper_url) DO NOTHING;
    """

    for paper in papers:

        cursor.execute(
            query,
            (
                paper["schemaVersion"],
                paper["recordType"],
                paper["title"],
                paper["authors"],
                paper["paper_url"],
                paper["github_url"],
                paper["github_stars"],
                paper["published_date"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Inserted {len(papers)} papers into PostgreSQL.")


if __name__ == "__main__":
    insert_papers()