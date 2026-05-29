# pareto-tournament

**Pareto selection for multi-objective agent optimization** — tournament selection on Pareto fronts with crowding distance and hypervolume indicators.

## What This Gives You

- **Pareto front computation** — identify non-dominated solutions
- **Tournament selection** — select agents based on multi-objective fitness
- **Crowding distance** — maintain diversity on the Pareto front
- **Hypervolume indicator** — measure quality of the Pareto approximation
- **Pure Python** — zero external dependencies

## How It Fits

Selection mechanism for the `ai-ranch` evolution cycles and `plato-training` evaluation. Uses `info-geo` for geometric distance computations.

## License

MIT
