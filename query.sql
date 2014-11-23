select conv_time,
offer_id,
MAX(CASE status WHEN 'Confirmed' THEN countstatus ELSE 0 END ) Confirmed,
MAX(CASE status WHEN 'Accepted' THEN countstatus ELSE 0 END ) Accepted,
(MAX(CASE status WHEN 'Confirmed' THEN countstatus ELSE 0 END )-MAX(CASE status WHEN 'Accepted' THEN countstatus ELSE 0 END)) diff,
url from
(select conv_time,offer_id, status, count(status) as countstatus, url from statustable group by offer_id, status) as statusgroup
group by offer_id