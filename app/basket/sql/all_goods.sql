SELECT
    m.medicine_id AS medicine_id,
    m.name AS medicine_name,
    m.manufactury_company AS manufacturer,
    s.quantity AS in_stock,
    m.price_per_unit AS unit_price
FROM
    medicine m
JOIN
    stock s ON m.medicine_id = s.medicine_id
WHERE
    s.cur_date = (
        SELECT MAX(cur_date)
        FROM stock
        WHERE medicine_id = m.medicine_id
    );
