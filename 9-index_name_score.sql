-- Creates an index named idx_name_first_score on the 'names' table.
-- This index is based on two columns:
-- 1. The first character of the 'name' column (using name(1)).
-- 2. The 'score' column.
CREATE INDEX idx_name_first_score ON names(name(1), score);
