API = "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"
api_key = API
query_skills = "SELECT DISTINCT job_role, job_description, responsibility, skillset from job_data WHERE lower(job_role) = '{}'"
query_about_company = "SELECT * from company_description_table WHERE LOWER(SPLIT_PART(company_name, ' ', 1)) = '{}'"
query_salary = '''
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