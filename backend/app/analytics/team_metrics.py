"""Team-level analytics calculations.

Analytics modules operate on stored SQLite data rather than calling external APIs.
"""

import pandas as pd


def compute_goal_differential_trend() -> pd.DataFrame:
    """Compute goal differential trend over time. Not yet implemented."""
    # TODO: Load game data from SQLite and compute rolling goal differential.
    return pd.DataFrame()


def compute_goals_scored_trend() -> pd.DataFrame:
    """Compute goals scored trend over time. Not yet implemented."""
    # TODO: Load game data from SQLite and compute goals scored per game.
    return pd.DataFrame()


def compute_goals_allowed_trend() -> pd.DataFrame:
    """Compute goals allowed trend over time. Not yet implemented."""
    # TODO: Load game data from SQLite and compute goals allowed per game.
    return pd.DataFrame()
