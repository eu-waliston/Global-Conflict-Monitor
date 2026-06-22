CREATE TABLE global_conflict_row (
    raw_id INT AUTO_INCREMENT PRIMARY KEY,

    conflict_id INT,
    location VARCHAR(255),

    side_a VARCHAR(255),
    side_b VARCHAR(255),

    year INT,

    type_of_conflicts VARCHAR(100),
    intensity_level VARCHAR(50)
);

DROP TABLE global_conflict_row;