USE global_conflict_monitor;


-- 🌎 REGIONS
CREATE TABLE IF NOT EXISTS regions (

    region_id INT AUTO_INCREMENT PRIMARY KEY,

    region_name VARCHAR(255) UNIQUE
);


-- 🌍 COUNTRIES
CREATE TABLE IF NOT EXISTS countries (

    country_id INT AUTO_INCREMENT PRIMARY KEY,

    country_name VARCHAR(255),

    region_id INT,

    FOREIGN KEY (region_id)
    REFERENCES regions(region_id)
);


-- ⚔️ CONFLICT TYPES
CREATE TABLE IF NOT EXISTS conflict_types (

    type_id INT AUTO_INCREMENT PRIMARY KEY,

    type_name VARCHAR(100)
);


-- 🔥 CONFLICTS

CREATE TABLE IF NOT EXISTS conflicts (

    conflict_id INT PRIMARY KEY,

    conflict_name VARCHAR(255),

    country_id INT,

    type_id INT,

    side_a VARCHAR(255),

    side_b VARCHAR(255),

    year INT,

    intensity_level INT,

    incompatibility VARCHAR(255),

    territory_name VARCHAR(255),

    start_date DATE,

    FOREIGN KEY (country_id)
    REFERENCES countries(country_id),

    FOREIGN KEY (type_id)
    REFERENCES conflict_types(type_id)
);


-- ☠️ FATALITIES

CREATE TABLE IF NOT EXISTS fatalities (

    fatality_id INT AUTO_INCREMENT PRIMARY KEY,

    conflict_id INT,

    deaths_best INT,

    deaths_low INT,

    deaths_high INT,

    FOREIGN KEY (conflict_id)
    REFERENCES conflicts(conflict_id)
);


-- 🧠 ACTORS

CREATE TABLE IF NOT EXISTS actors (

    actor_id INT AUTO_INCREMENT PRIMARY KEY,

    actor_name VARCHAR(255) UNIQUE,

    is_government_actor BOOLEAN
);


-- 🔗 CONFLICT ACTORS (N:N)

CREATE TABLE IF NOT EXISTS conflict_actors (

    conflict_id INT,

    actor_id INT,

    PRIMARY KEY (conflict_id, actor_id),

    FOREIGN KEY (conflict_id)
    REFERENCES conflicts(conflict_id),

    FOREIGN KEY (actor_id)
    REFERENCES actors(actor_id)
);