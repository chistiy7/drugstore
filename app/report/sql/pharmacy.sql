SELECT
    uo.order_date AS report_date,
    uol.medicine_name,
    SUM(uol.amount) AS total_amount_sold,
    m.price_per_unit,
    SUM(uol.amount * m.price_per_unit) AS total_revenue
FROM user_order_lines uol
JOIN user_order uo ON uol.order_id = uo.order_id
JOIN medicine m ON uol.medicine_name = m.name
WHERE MONTH(uo.order_date) = $e_month AND YEAR(uo.order_date) = $e_year
GROUP BY uo.order_date, uol.medicine_name, m.price_per_unit
ORDER BY uo.order_date;
