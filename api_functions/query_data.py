import psycopg2
queries = {
    "responsibilites_and_skills": "",
    "about_company": "",
    "salary":""
}
def execute_query(queries):
    db_params = {
        "host": "localhost",
        "port": "5432",
        "database": "postgres",
        "user": "postgres",
        "password": "JDCrafters"
    }
    # Create a connection to PostgreSQL
    connection = psycopg2.connect(
        host=db_params["host"],
        port=db_params["port"],
        database=db_params["database"],
        user=db_params["user"],
        password=db_params["password"]
    )

    cursor = connection.cursor()
    results = {}
    for query in queries:
        cursor.execute(queries[query])
        result = cursor.fetchall()
        if not result:
            print("no records found")
            result = None
        results[query] = result

    cursor.close()
    connection.close()
    return results

import json

if __name__ == "__main__":
    output = execute_query(query_dict)
    print(output)