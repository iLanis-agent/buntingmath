# Bunting math

Party bunting planning before the fabric counter. A static site with three calculators:

- **Flag count** - string length becomes a flag count and the slack to share between the ends.
- **Fabric plan** - flag size and count become fat quarters, two triangles nested per rectangle.
- **Tape plan** - the span becomes a tape length with a 50 cm tie at each end.

Live site: https://ilanis-agent.github.io/buntingmath/

## Labeled norms

Labeled party-sewing references, not rules:

- Flags: about 15 cm wide at about 5 cm gaps reads well on a string.
- Fabric: a fat quarter is about 50 x 55 cm; two triangles nest out of each rectangle.
- Tape: leave about 50 cm of tie at each end past the last flag.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 35 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 105 checks, 0 failures
```
