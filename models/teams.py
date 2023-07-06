teams = """
        CREATE TABLE IF NOT EXISTS teams (
             id INT AUTO_INCREMENT PRIMARY KEY,
             team_name VARCHAR(255),
             position INT,
             matches_played INT,
             games_won INT,
             games_matches INT,
             lost_games INT,
             goals_in_favor INT,
             goals_against INT,
             points INT
        )
    """