WITH ranked_salary AS (
    SELECT
        id,
        company,
        salary,
        ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary, id) AS row_num,
        COUNT(*)     OVER (PARTITION BY company)                     AS total_employees
    FROM Employee
)
SELECT id, company, salary
FROM ranked_salary
WHERE row_num BETWEEN total_employees / 2.0 AND total_employees / 2.0 + 1;
