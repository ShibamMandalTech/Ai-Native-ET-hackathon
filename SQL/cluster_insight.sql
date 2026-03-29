use newsroom;
CREATE TABLE cluster_insights (
    cluster_id INT PRIMARY KEY,
    summary TEXT,
    macro TEXT,
    sectors TEXT,
    experts TEXT,
    timeline TEXT,
    sentiment text,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);