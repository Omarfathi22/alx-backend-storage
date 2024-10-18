-- Rank country origins of bands by the number of 
-- SELECT band_name, (IFNULL(split, YEAR(CURRENT_DATE())) - formed) AS lifespan
SELECT origin, COUNT(*) AS nb_fans
    FROM metal_bands
    BY origin
    ORDER BY nb_fans DESC;
