SELECT
    m.name AS medicine_name,
    m.manufactury_company AS manufacturer,
--    s.quantity AS in_stock,
    m.price_per_unit AS unit_price
FROM
    stock s
JOIN
    medicine m ON s.medicine_id = m.medicine_id
WHERE
    m.name = '$e_medicine_name'
    AND s.cur_date = (
        SELECT MAX(cur_date)
        FROM stock
        WHERE medicine_id = s.medicine_id
    ); -- Выбираем только последнюю запись для каждого товара
