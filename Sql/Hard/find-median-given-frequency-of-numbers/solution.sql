WITH freq AS (
    SELECT
        num,
        frequency,
        SUM(frequency) OVER (ORDER BY num) AS cum_freq,
        SUM(frequency) OVER () AS total
    FROM Numbers
),
positions AS (
    SELECT
        num,
        cum_freq,
        frequency,
        FLOOR((total + 1) / 2.0) AS lower_pos,
        CEIL((total + 1) / 2.0)  AS upper_pos
    FROM freq
)
SELECT
    ROUND(AVG(num), 1) AS median
FROM positions
WHERE cum_freq >= lower_pos
  AND (cum_freq - frequency) < upper_pos;