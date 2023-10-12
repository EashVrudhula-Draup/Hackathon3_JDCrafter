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
    query = '''
    WITH temp AS (
        SELECT
            job_role,
            talent_cost,
            location_name,
            experience_range,
            currency,
            currency_code,
            experience,
            CASE
                WHEN TRIM(SPLIT_PART(experience_range, ' - ', 1)) ~ '^\d+(\.\d+)?$' THEN
                    CAST(SPLIT_PART(experience_range, ' - ', 1) AS numeric)
                ELSE NULL
            END AS x,
            CASE
                WHEN TRIM(SPLIT_PART(SPLIT_PART(experience_range, ' - ', 2), ' ', 1)) ~ '^\d+(\.\d+)?$' THEN
                    CAST(SPLIT_PART(SPLIT_PART(experience_range, ' - ', 2), ' ', 1) AS numeric)
                ELSE NULL
            END AS y
        FROM job_data
    ),



    cte AS (
        SELECT
            temp.job_role,
            experience,
            experience_range,
            temp.location_name,
            talent_cost,
            currency,
            currency_code,
            CASE
                WHEN temp.x IS NOT NULL AND temp.y IS NOT NULL THEN CAST(floor(((1.0 * temp.x) + temp.y::numeric) / 2) AS numeric)
                ELSE NULL
            END AS avg_exp
        FROM temp
    ),



    final AS (
        SELECT
            *,
            CASE
                WHEN experience IS NOT NULL AND experience = {exp} THEN talent_cost
                WHEN experience IS NULL AND experience_range IS NOT NULL AND avg_exp = {exp} THEN talent_cost
                ELSE NULL
            END AS talent_cost
        FROM cte
        WHERE job_role = '{job_role}' AND location_name = '{location_name}'
    )
    SELECT * FROM final
    '''

    output = execute_query({"query":
        query.format(job_role="Finance Manager", location_name="Fukui, Japan", exp=6)})
    print(output)