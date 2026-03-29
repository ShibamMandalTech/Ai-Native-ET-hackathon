SELECT 
    cluster_id, 
    COUNT(*) AS article_count,
    SUM(LENGTH(summary_points)) AS total_summary_chars,
    SUM(LENGTH(deep_content)) AS total_deep_content_chars
FROM newsroom.news 
WHERE cluster_id IS NOT NULL 
GROUP BY cluster_id 
ORDER BY article_count DESC;
