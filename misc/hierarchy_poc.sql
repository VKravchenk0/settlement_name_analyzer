-- VERSION WITH PATH
WITH RECURSIVE settlement_hierarchy AS (
    SELECT    id,
              name_lower,
              parent_id,
              '' AS path,
              '' as path_stripped,
              type as type_hierarchy,
              type,
              null as state,
              null as district,
              null as community
    FROM ua_settlements
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        s.id,
        s.name_lower,
        s.parent_id,
        CASE settlement_hierarchy.path
            WHEN '' THEN json_extract(s.public_name, '$.uk')
            ELSE settlement_hierarchy.path || ', ' || json_extract(s.public_name, '$.uk')
            END,
        CASE s.type
            WHEN 'STATE' THEN json_extract(s.public_name, '$.uk')
            WHEN 'DISTRICT' THEN settlement_hierarchy.path_stripped || ', ' || json_extract(s.public_name, '$.uk')
            ELSE settlement_hierarchy.path_stripped
            END,
        settlement_hierarchy.type_hierarchy || ', ' || s.type as type_hierarchy,
        s.type,
        -- calculating state
        CASE
            WHEN s.type = 'STATE' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('DISTRICT', 'COMMUNITY', 'CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then settlement_hierarchy.state
            ELSE null
            END as state,
        -- calculating district
        CASE
            WHEN s.type = 'DISTRICT' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('COMMUNITY', 'CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then settlement_hierarchy.district
            ELSE null
            END as district,
        -- calculating community
        CASE
            WHEN s.type = 'COMMUNITY' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then settlement_hierarchy.community
            ELSE null
            END as community

    FROM ua_settlements s,settlement_hierarchy
    WHERE s.parent_id = settlement_hierarchy.id
)
UPDATE ua_settlements
SET
    path = (SELECT path FROM settlement_hierarchy WHERE id=ua_settlements.id),
    state = (SELECT state FROM settlement_hierarchy WHERE id=ua_settlements.id),
    district = (SELECT district FROM settlement_hierarchy WHERE id=ua_settlements.id),
    community = (SELECT community FROM settlement_hierarchy WHERE id=ua_settlements.id);