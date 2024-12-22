SELECT *, `name`, `post` FROM `report_staff` r
JOIN `staff` s
ON r.idStaff = s.idStaff
WHERE 1=1
AND `month` = $e_month
AND `year` = $e_year;