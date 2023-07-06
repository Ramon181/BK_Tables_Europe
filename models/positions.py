positions = """
        CREATE TABLE IF NOT EXISTS positions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            league_id INT,
            team_id INT,
            FOREIGN KEY (team_id) REFERENCES teams (id),
            FOREIGN KEY (league_id) REFERENCES leagues (id)
        )
    """