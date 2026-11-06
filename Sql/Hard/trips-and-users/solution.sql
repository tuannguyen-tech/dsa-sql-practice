SELECT
    t.request_at AS "Day",
    ROUND(
        SUM(CASE
                WHEN t.status IN ('cancelled_by_driver', 'cancelled_by_client')
                THEN 1
                ELSE 0
            END)::numeric / COUNT(*),
        2
    ) AS "Cancellation Rate"
FROM Trips t
JOIN Users client
    ON t.client_id = client.users_id
JOIN Users driver
    ON t.driver_id = driver.users_id
WHERE client.banned = 'No'
  AND driver.banned = 'No'
  AND t.request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY t.request_at
ORDER BY t.request_at;