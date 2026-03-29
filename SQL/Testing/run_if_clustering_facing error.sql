SET SQL_SAFE_UPDATES = 0;
DELETE FROM newsroom.clusters;
UPDATE newsroom.news SET cluster_id = NULL, embedded = 0;