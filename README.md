# vequir-unit

VequIR's own units, as a product catalogue for the
[CAD tool](https://github.com/anroleroux/vequir-standard/tree/main/tools/cad): each product broken down into assemblies and parts,
written as CadQuery B-rep code from plain-language descriptions, built and
checked as exact solids, and assembled with its fit checked.

Product page: **[anroleroux.co.za/vequir-unit](https://anroleroux.co.za/vequir-unit/)**

## Products

- **PB6**, a powerbank: a six-cell 18650 pack in an enclosure, charged over
  USB-C and charging devices from two USB-A ports. This repository holds
  only the enclosure's own parts:
  - the **base** (`PB6/base`), driven by `l`, `b`, `h` and `wall`;
  - the **lid** (`PB6/lid`), sized from the base.

  `PB6/assembly.py`, the one assembly, places them with the six-cell pack
  from vequir-power (`battery_holders/pack_3x2`), screwed to the base's four
  pillars, and the bought-in CN3302 and IP6505 charger boards and M1.2
  screws from vequir-standard (`power/…`, `hardware/…`), and the build checks
  the fit.

## The breakdown

```
products/<PRODUCT>/product.md                               "# Title", then a blurb
products/<PRODUCT>/assembly.py                              optional: the whole product, assembled
products/<PRODUCT>/<part>/part.py                           a part of the product itself
products/<PRODUCT>/<assembly>/assembly.md                   "# Title", then a blurb
products/<PRODUCT>/<assembly>/<sub>/.../assembly.md          sub-assemblies, any depth
products/<PRODUCT>/<assembly>/.../<part>/description.md     the natural-language description
products/<PRODUCT>/<assembly>/.../<part>/part.py            the CadQuery script (B-rep code)
```

- A product holds assemblies, and parts of its own (`PB6/lid`).
- An assembly holds either sub-assemblies or parts (it is a leaf), never both.
- A part is any directory with a `part.py`.
- An assembly may also hold an `assembly.py`, its assembled model, checked
  for interference (parts sharing volume) and contact (parts touching over
  an area). The site shows it above the parts.
- Any script can call `load_part("../base")` to run another part's script
  and read its variables, and `load_library("<category>/<item>")` for a
  library item. The libraries are vequir-power's and vequir-standard's, which
  `libraries.txt` names; this repository has no library of its own.

A part's **designation** is its path, for example `PB6/base`; an
assembly's is its path too (`PB6`). Product directories keep their
code (`PB6`); assembly and part slugs are lowercase with underscores.
Titles come from `product.md`, `assembly.md` and the first line of a part
script's docstring.

## Working on it

Clone the libraries `libraries.txt` names beside this repository, install
the CAD tool (it comes with vequir-standard, under `tools/cad/`),
and run everything from this repository's root:

```bash
git clone https://github.com/anroleroux/vequir-power ../vequir-power
git clone https://github.com/anroleroux/vequir-standard ../vequir-standard
python -m venv .venv && source .venv/bin/activate
pip install -e "../vequir-standard/tools/cad[dev]"

python -m pytest -q tests                     # checks of the real parts
cad build PB6/base                              # one part
cad build PB6                                   # an assembled model
cad site --out results --site site      # every part, then the pages
```

`results/` and `site/` are build output and git-ignored. In a Claude Code
session, the `cad-part` skill (`.claude/skills/cad-part/`) takes
a designation plus modelling instructions through the same steps.

## CI and the product page

`.github/workflows/cad.yml` runs on every push to `main` and `claude/**`. It
clones the libraries this repository uses beside the checkout
(the branch of the same name when it exists there, else the default branch),
installs the CAD tool from vequir-standard's clone, runs the tests, builds every part, and deploys the site to GitHub Pages:
**anroleroux.co.za/vequir-unit**, the product page. A part that fails to
build fails the job.
Settings → Pages → Source must be GitHub Actions.

Actions → **cad** → *Run workflow*, with `design` set to a part directory
holding a `description.md`, has Claude write its script; it needs the
`ANTHROPIC_API_KEY` repository secret.
