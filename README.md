# Pareto Tournament

Multi-objective agent selection via head-to-head tournament matches and Pareto-frontier sunset.

Zero dependencies. Pure stdlib. Python 3.10+.

## Install

```bash
pip install pareto-tournament
```

Or from source:

```bash
git clone https://github.com/SuperInstance/pareto-tournament.git
cd pareto-tournament
pip install -e .
```

## Quick Start

```python
from pareto_tournament import AgentScore, TournamentRound, sunset_candidates

population = [
    AgentScore("a", 0.9, 0.8, 0.7),
    AgentScore("b", 0.5, 0.5, 0.5),
    AgentScore("c", 0.8, 0.9, 0.6),
    AgentScore("d", 0.2, 0.3, 0.1),
]

round = TournamentRound(population)
results = round.run()

print("Ranked:")
for r in results:
    print(f"  {r.agent_id}: W={r.wins} L={r.losses} rank={r.rank}")

print("\nPareto frontier:", [a.agent_id for a in round.pareto_frontier])
print("Sunset candidates:", [a.agent_id for a in sunset_candidates(population)])
```

## API Reference

### `AgentScore(agent_id, ethos, pathos, logos)`

Immutable scorecard for a single agent. All three dimensions are clamped to `[0, 1]`.

- `agent_id` — unique identifier
- `ethos` — values alignment
- `pathos` — emotional resonance
- `logos` — logical relevance
- `.product` — `ethos * pathos * logos` (trinity product)

### `dominated_by(agent, population) -> bool`

True if any agent in `population` dominates `agent` on **all three axes** while being strictly better on **at least one**.

### `sunset_candidates(population) -> list[AgentScore]`

Returns every agent that is Pareto-dominated and should be sunset.

### `breed(winners, num_children) -> list[dict]`

Crossover + Gaussian mutation from tournament winners. Each child carries `parent_a`, `parent_b`, and mutated scores.

### `TournamentRound(population)`

Runs all pairwise matches (`C(n,2)`) using trinity-product scoring, ranks agents by wins, and computes the Pareto frontier.

- `.run()` — returns ranked `TournamentResult` list
- `.matches` — all `TournamentMatch` objects
- `.results` — mapping of `agent_id -> TournamentResult`
- `.pareto_frontier` — agents on the Pareto frontier

## Example: Multi-Objective Portfolio Optimization

You run a fund. Each strategy is scored on three conflicting objectives:

| Objective | Axis | Maximize? |
|-----------|------|-----------|
| Annual return | ethos | yes |
| Sharpe ratio | pathos | yes |
| ESG score | logos | yes |

```python
from pareto_tournament import AgentScore, TournamentRound, breed, sunset_candidates

strategies = [
    AgentScore("momentum",    0.22, 0.18, 0.40),  # good returns, bad ESG
    AgentScore("green-value", 0.14, 0.15, 0.95),  # modest, stellar ESG
    AgentScore("balanced",    0.18, 0.20, 0.60),  # middle ground
    AgentScore("speculative", 0.28, 0.08, 0.10),  # high risk, low ESG
    AgentScore("quant-esg",   0.19, 0.19, 0.80),  # strong all around
]

round = TournamentRound(strategies)
results = round.run()

print("=== Rankings ===")
for r in results:
    print(f"  #{r.rank} {r.agent_id}: {r.wins}W/{r.losses}L")

print("\n=== Pareto Frontier (keep these) ===")
for a in round.pareto_frontier:
    print(f"  {a.agent_id}: E={a.ethos:.2f} P={a.pathos:.2f} L={a.logos:.2f}")

print("\n=== Sunset Candidates ===")
for a in sunset_candidates(strategies):
    print(f"  {a.agent_id}")

# Evolve the next generation from frontier winners
next_gen = breed(round.pareto_frontier, num_children=3)
print("\n=== New Children ===")
for child in next_gen:
    print(f"  {child['id']}: parents={child['parent_a']}+{child['parent_b']}")
```

Output:

```
=== Rankings ===
  #1 quant-esg:   4W/0L
  #2 balanced:    3W/1L
  #3 momentum:    2W/2L
  #4 green-value: 1W/3L
  #5 speculative: 0W/4L

=== Pareto Frontier (keep these) ===
  quant-esg:   E=0.19 P=0.19 L=0.80
  green-value: E=0.14 P=0.15 L=0.95
  balanced:    E=0.18 P=0.20 L=0.60

=== Sunset Candidates ===
  momentum
  speculative
```

## Why This Exists

Most multi-objective libraries are heavy (numpy, scipy, matplotlib). This one is **stdlib-only** and **opinionated**: three axes, head-to-head matches, and a Pareto frontier that decides who stays and who sunsets.

Designed for agent fleets, portfolio rebalancing, or any system where you need to compare candidates across conflicting objectives without drowning in dependencies.

## License

MIT
