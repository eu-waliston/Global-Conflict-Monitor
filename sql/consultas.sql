# Conflitos por país
SELECT c.country_name, COUNT(*) AS total_conflicts FROM conflicts cf JOIN countries c ON cf.country_id = c.country_id GROUP BY c.country_name ORDER BY total_conflicts DESC;

# Conflitos de alta intensidade
SELECt * FROM conflicts WHERE intensity_level = 'High';

# Quantidade de conflitos por ano
SELECT year, COUNT(*) AS total FROM conflicts GROUP BY year ORDER BY year;
