# ASC Karnaugh – minimizing a Boolean function starting from a name

Project for the Computer Systems Architecture (ASC) course, first year.
Starting from the letters of a name, the program builds a Boolean function of 4 variables,
minimizes it with the Veitch-Karnaugh method (implemented with the Quine-McCluskey algorithm)
and draws the logic diagram of the minimal form.

## How it works

1. Each letter gets its position in the Romanian alphabet of 31 letters
   (A = 1, Ă = 2, ..., Z = 31).
2. The index is reduced modulo 16 and written in hexadecimal and as a 4-bit binary number (`ABCD`, `A` = most significant bit).
   The resulting value is a **minterm** of the function `f(A, B, C, D)`.
3. The unique minterms become the cells containing `1` in the Karnaugh map (at least 8 are required; if the name
   is not enough, extra letters can be appended with `--extra`).
4. The prime implicants and the minimal sum-of-products forms are computed.
5. The minimal form is checked against all 16 input combinations and drawn as a logic diagram
   (inverters, AND gates, one OR gate).

## Usage

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python main.py SIMION --extra ESCU
```

Options:

| Option | Description |
|---|---|
| `name` | surname (letters of the Romanian alphabet) |
| `--extra LETTERS` | letters appended to the name to reach at least 8 unique values |
| `--schema FILE` | where the logic diagram is saved (default `schema.png`) |
| `--no-schema` | do not generate the image |

## Example (`SIMION` + `ESCU`)

```
Unique minterms (8): [0, 1, 2, 5, 6, 7, 10, 11]

CD\AB |  00    01    11    10
 00   | 1(p0)  0(p4)  0(p12) 0(p8)
 01   | 1(p1)  1(p5)  0(p13) 0(p9)
 11   | 0(p3)  1(p7)  0(p15) 1(p11)
 10   | 1(p2)  1(p6)  0(p14) 1(p10)

Minimal sum-of-products forms:
  1. f = A'B'C' + A'CD' + A'BD + AB'C
  2. f = A'B'D' + A'C'D + A'BC + AB'C
```

A prime (`'`) denotes negation. The minimal cover is not unique: both forms have the same cost,
and the program draws the first one.

Generated diagram: [`docs/schema.png`](docs/schema.png). The accompanying report (in Romanian, PDF): [`docs/ASC_Referat_1.pdf`](docs/ASC_Referat_1.pdf).

## Project structure

```
main.py            command-line interface
logic.py           letter indexing, Quine-McCluskey, Karnaugh map
draw.py            logic diagram drawing (matplotlib)
tests/             unit tests
docs/              the report and the generated diagram
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT, see [LICENSE](LICENSE).
