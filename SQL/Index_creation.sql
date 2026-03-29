CREATE INDEX idx_news_embedded ON news(embedded);
CREATE INDEX idx_news_cluster ON news(cluster_id);

CREATE INDEX idx_engagement_user ON engagement(user_id);
CREATE INDEX idx_engagement_video ON engagement(video_id);

CREATE INDEX idx_videos_news ON videos(news_id);