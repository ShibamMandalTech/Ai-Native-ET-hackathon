CREATE TABLE news (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    url VARCHAR(500),
    category VARCHAR(500),
    content VARCHAR(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    retries INT DEFAULT 0,
    deep_content LONGTEXT,
    summary_points TEXT,
    processing_stage VARCHAR(50),
    embedded TINYINT(1) DEFAULT 0,
    cluster_id INT,
    video_status VARCHAR(50),
    FOREIGN KEY (cluster_id) REFERENCES clusters(id) ON DELETE SET NULL
);
ALTER TABLE news ADD COLUMN deep_content TEXT;
ALTER TABLE news ADD COLUMN deep_status VARCHAR(20) DEFAULT 'pending';