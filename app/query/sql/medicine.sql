SELECT
    m.medicine_id,
    m.name AS medicine_name,
    m.manufactury_company,
    m.manufactory_country,
    s.quantity,
    s.cur_date AS last_date
FROM medicine m
JOIN stock s ON m.medicine_id = s.medicine_id
WHERE m.name = '$input_medicine'
  AND s.cur_date = (
      SELECT MAX(sub_s.cur_date)
      FROM stock sub_s
      WHERE sub_s.medicine_id = m.medicine_id
  );