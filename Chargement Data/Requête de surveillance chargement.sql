SELECT 'user', COUNT(*) FROM PUBLIC."User"

UNION

SELECT 'course', COUNT(*) FROM PUBLIC."course"

UNION

SELECT 'Result', COUNT(*) FROM PUBLIC."Result"

UNION

SELECT 'Fil', COUNT(*) FROM PUBLIC."Threads"

UNION

SELECT 'messagemessage', COUNT(*) FROM PUBLIC."message"