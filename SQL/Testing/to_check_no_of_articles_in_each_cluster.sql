SELECT 
    cluster_id, 
    COUNT(*) as article_count 
FROM newsroom.news 
WHERE cluster_id IS NOT NULL 
GROUP BY cluster_id 
ORDER BY article_count DESC;
