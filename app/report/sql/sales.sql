SELECT *, name_o, price_o FROM sales_report r
JOIN stock p
ON r.prodID = p.prodID
WHERE 1=1
AND mes_o = $e_month
AND god_o = $e_year;