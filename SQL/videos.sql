use newsroom;
CREATE TABLE videos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    news_id BIGINT,
    script TEXT,
    audio_path VARCHAR(255),
    video_path VARCHAR(255),
    duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
);