USE global_conflict_monitor;

INSERT INTO countries (country_name)
SELECT DISTINCT location
FROM global_conflicts_raw;

INSERT INTO conflict_types (type_name)
SELECT DISTINCT type_of_conflict
FROM global_conflicts_raw;