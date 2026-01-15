SELECT
    m.member_id,
    m.name,
    p.persona,
    p.confidence AS persona_confidence,
    m.last_active,
    GROUP_CONCAT(s.skill_name, ', ') AS skills
FROM members m
JOIN persona_analysis p
    ON m.member_id = p.member_id
LEFT JOIN member_skills ms
    ON m.member_id = ms.member_id
LEFT JOIN skills s
    ON ms.skill_id = s.skill_id
WHERE p.persona = 'Mentor Material'
ORDER BY
    p.confidence DESC,
    m.last_active DESC;
