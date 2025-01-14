SELECT report_month, report_year, new_users, total_orders
FROM user_report
WHERE report_month = $e_month AND report_year = $e_year;
