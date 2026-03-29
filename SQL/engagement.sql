CREATE TABLE engagement (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    video_id BIGINT,
    news_id BIGINT,
    watch_time FLOAT,
    liked BOOLEAN DEFAULT FALSE,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
);