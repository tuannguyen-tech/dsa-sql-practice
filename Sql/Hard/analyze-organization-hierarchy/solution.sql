
WITH RECURSIVE
hierarchy_levels AS (
    SELECT
        employee_id,
        employee_name,
        1 AS level
    FROM Employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.employee_name,
        h.level + 1
    FROM Employees e
    JOIN hierarchy_levels h ON e.manager_id = h.employee_id
),
manager_descendants AS (
    SELECT
        employee_id AS manager_id,
        employee_id,
        salary
    FROM Employees

    UNION ALL

    SELECT
        md.manager_id,
        e.employee_id,
        e.salary
    FROM manager_descendants md
    JOIN Employees e ON md.employee_id = e.manager_id
),
aggregated AS (
    SELECT
        manager_id AS employee_id,
        COUNT(*) - 1 AS team_size,
        SUM(salary) AS budget
    FROM manager_descendants
    GROUP BY manager_id
)
SELECT
    h.employee_id,
    h.employee_name,
    h.level,
    COALESCE(a.team_size, 0) AS team_size,
    COALESCE(a.budget, h.salary) AS budget
FROM hierarchy_levels h
LEFT JOIN aggregated a ON h.employee_id = a.employee_id
ORDER BY
    h.level ASC,
    budget DESC,
    h.employee_name ASC;