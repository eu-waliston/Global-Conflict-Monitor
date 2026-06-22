-- =====================================================
-- 🌍 GLOBAL CONFLICT MONITOR
-- insert_normalized_data.sql
-- =====================================================

USE global_conflict_monitor;

-- =====================================================
-- 🌎 REGIONS
-- =====================================================

INSERT IGNORE INTO regions (region_name)

SELECT DISTINCT region
FROM global_conflict_raw
WHERE region IS NOT NULL;

-- =====================================================
-- 🌍 COUNTRIES
-- =====================================================

INSERT IGNORE INTO countries (
    country_name,
    region_id
)

SELECT DISTINCT
    g.location,

    r.region_id

FROM global_conflict_raw g

JOIN regions r
ON g.region = r.region_name

WHERE g.location IS NOT NULL;

-- =====================================================
-- ⚔️ CONFLICT TYPES
-- =====================================================

INSERT IGNORE INTO conflict_types (
    type_name
)

SELECT DISTINCT type_of_conflict
FROM global_conflict_raw
WHERE type_of_conflict IS NOT NULL;

-- =====================================================
-- 🔥 CONFLICTS
-- =====================================================

INSERT IGNORE INTO conflicts (

    conflict_id,
    conflict_name,
    country_id,
    type_id,
    side_a,
    side_b,
    year,
    intensity_level,
    incompatibility,
    territory_name,
    start_date
)

SELECT DISTINCT

    g.conflict_id,

    CONCAT(g.side_a, ' vs ', g.side_b),

    c.country_id,

    ct.type_id,

    g.side_a,

    g.side_b,

    g.year,

    g.intensity_level,

    g.incompatibility,

    g.territory_name,

    STR_TO_DATE(g.start_date, '%Y-%m-%d')

FROM global_conflict_raw g

JOIN countries c
ON g.location = c.country_name

JOIN conflict_types ct
ON g.type_of_conflict = ct.type_name;

-- =====================================================
-- ☠️ FATALITIES
-- =====================================================

INSERT IGNORE INTO fatalities (

    conflict_id,
    deaths_best,
    deaths_low,
    deaths_high
)

SELECT DISTINCT

    conflict_id,

    intensity_level * 1000,

    intensity_level * 500,

    intensity_level * 2000

FROM global_conflict_raw;

-- =====================================================
-- 🧠 ACTORS
-- =====================================================

INSERT IGNORE INTO actors (
    actor_name,
    is_government_actor
)

SELECT DISTINCT
    side_a,
    TRUE

FROM global_conflict_raw

WHERE side_a IS NOT NULL;

INSERT IGNORE INTO actors (
    actor_name,
    is_government_actor
)

SELECT DISTINCT
    side_b,
    FALSE

FROM global_conflict_raw

WHERE side_b IS NOT NULL;

-- =====================================================
-- 🔗 CONFLICT ACTORS
-- =====================================================

INSERT IGNORE INTO conflict_actors (
    conflict_id,
    actor_id
)

SELECT DISTINCT

    g.conflict_id,

    a.actor_id

FROM global_conflict_raw g

JOIN actors a
ON g.side_a = a.actor_name;

INSERT IGNORE INTO conflict_actors (
    conflict_id,
    actor_id
)

SELECT DISTINCT

    g.conflict_id,

    a.actor_id

FROM global_conflict_raw g

JOIN actors a
ON g.side_b = a.actor_name;