WITH RECURSIVE settlement_hierarchy AS (
    SELECT    id,
              null as state,
              null as district,
              null as community
    FROM ua_settlements
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        s.id,
        -- calculating state
        CASE
            WHEN s.type = 'STATE' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('DISTRICT', 'COMMUNITY', 'CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then parent.state
            ELSE null
            END as state,
        -- calculating district
        CASE
            WHEN s.type = 'DISTRICT' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('COMMUNITY', 'CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then parent.district
            ELSE null
            END as district,
        -- calculating community
        CASE
            WHEN s.type = 'COMMUNITY' THEN json_extract(s.public_name, '$.uk')
            WHEN s.type in ('CITY', 'URBAN', 'SETTLEMENT', 'VILLAGE') then parent.community
            ELSE null
            END as community

    FROM ua_settlements s, settlement_hierarchy parent
    WHERE s.parent_id = parent.id
)
UPDATE ua_settlements
SET
    state = (SELECT state FROM settlement_hierarchy WHERE id=ua_settlements.id),
    district = (SELECT district FROM settlement_hierarchy WHERE id=ua_settlements.id),
    community = (SELECT community FROM settlement_hierarchy WHERE id=ua_settlements.id);