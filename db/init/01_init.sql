-- Jenkins Dashboard Database Initialization
-- This script creates the necessary tables for the Jenkins Dashboard application

-- Create jenkins_items table with all required columns
CREATE TABLE IF NOT EXISTS jenkins_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    url TEXT NOT NULL,
    type VARCHAR(200),
    description TEXT,
    last_build_status VARCHAR(50),
    last_build_url TEXT,
    folder VARCHAR(500),
    timestamp DOUBLE PRECISION,
    is_disabled BOOLEAN DEFAULT FALSE,
    last_build_date TIMESTAMP WITH TIME ZONE,
    last_successful_date TIMESTAMP WITH TIME ZONE,
    last_failed_date TIMESTAMP WITH TIME ZONE,
    days_since_last_build INTEGER,
    total_builds INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    success_rate DECIMAL(10,2) DEFAULT 0.0,
    is_test_job BOOLEAN DEFAULT FALSE,
    last_build_duration BIGINT DEFAULT 0,
    last_successful_duration BIGINT DEFAULT 0,
    last_failed_duration BIGINT DEFAULT 0,
    avg_build_duration DECIMAL(10,2) DEFAULT 0.0,
    avg_successful_duration DECIMAL(10,2) DEFAULT 0.0,
    avg_failed_duration DECIMAL(10,2) DEFAULT 0.0,
    min_build_duration BIGINT DEFAULT 0,
    max_build_duration BIGINT DEFAULT 0,
    total_build_duration BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_jenkins_items_name ON jenkins_items(name);
CREATE INDEX IF NOT EXISTS idx_jenkins_items_folder ON jenkins_items(folder);
CREATE INDEX IF NOT EXISTS idx_jenkins_items_status ON jenkins_items(last_build_status);
CREATE INDEX IF NOT EXISTS idx_jenkins_items_timestamp ON jenkins_items(timestamp);
CREATE INDEX IF NOT EXISTS idx_jenkins_items_is_disabled ON jenkins_items(is_disabled);
CREATE INDEX IF NOT EXISTS idx_jenkins_items_is_test_job ON jenkins_items(is_test_job);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_jenkins_items_updated_at 
    BEFORE UPDATE ON jenkins_items 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create a view for recent jobs (last 30 days)
CREATE OR REPLACE VIEW recent_jobs AS
SELECT * FROM jenkins_items 
WHERE last_build_date >= CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY last_build_date DESC;

-- Create a view for inactive jobs
CREATE OR REPLACE VIEW inactive_jobs AS
SELECT * FROM jenkins_items 
WHERE days_since_last_build > 60
ORDER BY days_since_last_build DESC;

-- Create a view for test jobs
CREATE OR REPLACE VIEW test_jobs AS
SELECT * FROM jenkins_items 
WHERE is_test_job = TRUE
ORDER BY name;

-- Create a view for disabled jobs
CREATE OR REPLACE VIEW disabled_jobs AS
SELECT * FROM jenkins_items 
WHERE is_disabled = TRUE
ORDER BY name;

-- Create a view for jobs without descriptions
CREATE OR REPLACE VIEW jobs_without_description AS
SELECT * FROM jenkins_items 
WHERE description IS NULL OR description = ''
ORDER BY name;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jenkins_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jenkins_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO jenkins_user; 