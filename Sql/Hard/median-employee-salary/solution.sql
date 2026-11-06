WITH ranked AS (
    SELECT
        id,
        company,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY company
            ORDER BY salary, id
        ) AS rn,
        COUNT(*) OVER (PARTITION BY company) AS cnt
    FROM Employee
)
SELECT
    id,
    company,
    salary
FROM ranked
WHERE
    (cnt % 2 = 1 AND rn = (cnt + 1) / 2)
    OR
    (cnt % 2 = 0 AND rn IN (cnt / 2, cnt / 2 + 1))
ORDER BY company, salary;