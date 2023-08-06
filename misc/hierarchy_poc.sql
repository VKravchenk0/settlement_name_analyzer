WITH RECURSIVE settlement_hierarchy AS (
    SELECT    id,
              name_lower,
              parent_id,
              '' AS path,
              '' as path_stripped,
              type
    FROM ua_settlements
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        s.id,
        s.name_lower,
        s.parent_id,
--         settlement_hierarchy.path || ', ' || s.name_lower
        settlement_hierarchy.path || ', ' || json_extract(s.public_name, '$.uk'),
        CASE s.type
            WHEN 'STATE' THEN json_extract(s.public_name, '$.uk')
            ELSE settlement_hierarchy.path_stripped
        END,
        settlement_hierarchy.type || ', ' || s.type
    FROM ua_settlements s,settlement_hierarchy
    WHERE s.parent_id = settlement_hierarchy.id
)
SELECT *
FROM settlement_hierarchy where id in (
    select id from ua_settlements where name_lower = 'лебедин' order by name_lower
    );