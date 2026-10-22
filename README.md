# MahjongPY

A first MVP for estimating dangerous tiles in Japanese/Riichi Mahjong from visible game information.

This program does **not** identify an opponent's exact concealed hand. It uses transparent deterministic heuristics to rank tiles by approximate danger. Results are useful for experimentation and decision support, not guaranteed probabilities.

## Run

With Python 3.10+:

```bash
python -m mahjong_inference.cli --discards 1m,2m,9p,E,S --riichi
```

Optional arguments:

- `--melds '2m,3m,4m;E,E,E'`
- `--known '5m,5m,7p'`
- `--limit 15`

After installation, the equivalent console command is:

```bash
pip install -e .
mahjong-danger --discards 1m,2m,9p,E,S --riichi
```

## Current model

The estimator considers visible copies, repeated discards, neighboring suited tiles, terminals/honors, open melds, and riichi. Scores are normalized over all 34 tile types and include explanations.

## Development

```bash
python -m unittest discover -s tests -v
```

Future work includes shanten/wait calculation, candidate-hand generation, yaku and score estimation, learned discard-pattern models, and screenshot recognition.
