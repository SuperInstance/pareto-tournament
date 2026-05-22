"""Pareto Tournament — multi-objective selection via head-to-head competition.

A zero-dependency Python library for Pareto-frontier selection,
tournament-style breeding, and graceful sunset of dominated agents.
"""

from .core import (
    AgentScore,
    TournamentMatch,
    TournamentResult,
    TournamentRound,
    breed,
    dominated_by,
    sunset_candidates,
)

__all__ = [
    "AgentScore",
    "TournamentMatch",
    "TournamentResult",
    "TournamentRound",
    "breed",
    "dominated_by",
    "sunset_candidates",
]

__version__ = "0.1.0"
