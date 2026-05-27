"""Tests for pareto_tournament.core.

Run with: pytest
"""

import random

import pytest

from pareto_tournament.core import (
    AgentScore,
    TournamentMatch,
    TournamentRound,
    breed,
    dominated_by,
    sunset_candidates,
)


class TestAgentScore:
    def test_valid_initialization(self):
        s = AgentScore("a", 0.5, 0.6, 0.7)
        assert s.agent_id == "a"
        assert s.ethos == 0.5
        assert s.pathos == 0.6
        assert s.logos == 0.7

    def test_product(self):
        s = AgentScore("a", 0.5, 0.5, 0.5)
        assert s.product == 0.125

    def test_zero_product(self):
        s = AgentScore("a", 0.0, 1.0, 1.0)
        assert s.product == 0.0

    def test_value_out_of_range(self):
        with pytest.raises(ValueError, match="ethos"):
            AgentScore("a", 1.5, 0.5, 0.5)

    def test_negative_value(self):
        with pytest.raises(ValueError, match="pathos"):
            AgentScore("a", 0.5, -0.1, 0.5)


class TestDominatedBy:
    def test_self_not_dominated(self):
        a = AgentScore("a", 0.5, 0.5, 0.5)
        assert not dominated_by(a, [a])

    def test_strictly_dominated(self):
        a = AgentScore("a", 0.5, 0.5, 0.5)
        b = AgentScore("b", 0.6, 0.6, 0.6)
        assert dominated_by(a, [a, b])
        assert not dominated_by(b, [a, b])

    def test_not_dominated_when_one_axis_lower(self):
        a = AgentScore("a", 0.5, 0.5, 0.5)
        b = AgentScore("b", 0.6, 0.6, 0.4)
        assert not dominated_by(a, [a, b])
        assert not dominated_by(b, [a, b])

    def test_not_dominated_when_equal(self):
        a = AgentScore("a", 0.5, 0.5, 0.5)
        b = AgentScore("b", 0.5, 0.5, 0.5)
        assert not dominated_by(a, [a, b])

    def test_multiple_agents(self):
        a = AgentScore("a", 0.3, 0.3, 0.3)
        b = AgentScore("b", 0.5, 0.5, 0.5)
        c = AgentScore("c", 0.4, 0.4, 0.4)
        assert dominated_by(a, [a, b, c])
        assert not dominated_by(b, [a, b, c])
        assert dominated_by(c, [a, b, c])


class TestSunsetCandidates:
    def test_all_frontier(self):
        a = AgentScore("a", 0.5, 0.5, 0.5)
        b = AgentScore("b", 0.5, 0.6, 0.4)
        c = AgentScore("c", 0.6, 0.5, 0.4)
        assert sunset_candidates([a, b, c]) == []

    def test_some_dominated(self):
        a = AgentScore("a", 0.3, 0.3, 0.3)
        b = AgentScore("b", 0.6, 0.6, 0.6)
        result = sunset_candidates([a, b])
        assert result == [a]


class TestTournamentMatch:
    def test_resolve(self):
        m = TournamentMatch("a", "b", scores={"a": 0.8, "b": 0.5})
        assert m.resolve() == "a"
        assert m.winner == "a"

    def test_resolve_tie_wins_lexicographically(self):
        m = TournamentMatch("a", "b", scores={"a": 0.5, "b": 0.5})
        # max() picks the first when equal
        assert m.resolve() == "a"

    def test_no_scores_raises(self):
        m = TournamentMatch("a", "b")
        with pytest.raises(ValueError, match="No scores"):
            m.resolve()


class TestTournamentRound:
    def test_run_ranks_all(self):
        agents = [
            AgentScore("a", 0.9, 0.9, 0.9),
            AgentScore("b", 0.1, 0.1, 0.1),
            AgentScore("c", 0.5, 0.5, 0.5),
        ]
        round_ = TournamentRound(agents)
        results = round_.run()
        assert len(results) == 3
        assert results[0].agent_id == "a"
        assert results[0].rank == 1
        assert results[1].agent_id == "c"
        assert results[2].agent_id == "b"

    def test_pareto_frontier_computed(self):
        agents = [
            AgentScore("a", 0.9, 0.9, 0.9),
            AgentScore("b", 0.1, 0.1, 0.1),
            AgentScore("c", 0.5, 0.95, 0.4),
            AgentScore("d", 0.95, 0.4, 0.4),
        ]
        round_ = TournamentRound(agents)
        round_.run()
        frontier = round_.pareto_frontier
        ids = {a.agent_id for a in frontier}
        assert "a" in ids
        assert "b" not in ids
        assert "c" in ids
        assert "d" in ids

    def test_matches_are_all_pairs(self):
        agents = [
            AgentScore("a", 0.5, 0.5, 0.5),
            AgentScore("b", 0.5, 0.5, 0.5),
            AgentScore("c", 0.5, 0.5, 0.5),
        ]
        round_ = TournamentRound(agents)
        round_.run()
        assert len(round_.matches) == 3  # C(3,2)


class TestBreed:
    def test_two_parents(self):
        random.seed(0)
        a = AgentScore("a", 0.9, 0.8, 0.7)
        b = AgentScore("b", 0.3, 0.4, 0.5)
        children = breed([a, b], num_children=2)
        assert len(children) == 2
        for child in children:
            assert "id" in child
            assert child["parent_a"] in ("a", "b")
            assert child["parent_b"] in ("a", "b")
            assert 0.0 <= child["ethos"] <= 1.0
            assert 0.0 <= child["pathos"] <= 1.0
            assert 0.0 <= child["logos"] <= 1.0

    def test_single_parent_clone(self):
        random.seed(1)
        a = AgentScore("a", 0.5, 0.5, 0.5)
        children = breed([a], num_children=3)
        assert len(children) == 3
        for child in children:
            assert child["parent_a"] == "a"
            assert child["parent_b"] is None

    def test_zero_winners(self):
        children = breed([], num_children=1)
        assert len(children) == 1
        assert children[0]["parent_a"] is None


class TestTrinityProduct:
    def test_trinity_product_ranking(self):
        """Ensure product correctly distinguishes agents."""
        a = AgentScore("a", 1.0, 1.0, 1.0)
        b = AgentScore("b", 0.5, 1.0, 1.0)
        c = AgentScore("c", 0.5, 0.5, 0.5)
        assert a.product > b.product > c.product
