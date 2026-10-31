# Daneel — Computational Astrophysics 2026–27

A teaching package for modelling exoplanet transits and building detection
pipelines. The repository contains the course example code, a runnable CLI,
and Sphinx documentation.

Documentation: <https://tiziano1590.github.io/comp_astro_26/>.

## Installation

### Prerequisites

- Python >= 3.10

### Install from source

```bash
git clone https://github.com/tiziano1590/comp_astro_26.git
cd comp_astro_26
pip install .
```

### Development installation

```bash
pip install -e '.[dev,docs]'
```

## Usage

After installation, you can run daneel from the command line:

```bash
daneel -i <input_file> --transit [--output lightcurve.png]
```

Daneel can only be run from the command line after proper installation. Alternatively, daneel can be run with the command:

```bash
python [PATH TO DANEEL SRC]/src/daneel/__main__.py -i <input_file> --transit [--output lightcurve.png]
```

### Command-line options

- `-i, --input`: Input parameter file (required)
- `-t, --transit`: Generate a transit light curve from the YAML input
- `-d, --detect`: Reserved for the course detection exercise
- `-a, --atmosphere`: Reserved for the course atmosphere exercise
- `-o, --output`: Output path for the transit plot (default: `lc.png`)

### Examples

```bash
# Plot light curve of K2-18b from parameter file
daneel -i examples/K2-18b.yaml --transit --output K2-18b_lightcurve.png
# Can run this command with a parameter file outside of the github repository, if path is provided

# Run exoplanet detection
daneel -i examples/params.yaml --transit --output lightcurve.png

# Run atmospheric characterization
daneel -i examples/params.yaml --detect

# Run both detection and atmospheric analysis
daneel -i examples/params.yaml --atmosphere
```

## Input File Format

The input file should be a YAML file containing the necessary parameters for the analysis.

## Development

Run the test suite and style checks with:

```bash
pytest
ruff check .
```

Build the documentation with `make -C docs html`.

## License

This project is licensed under the GNU General Public License v3.0.

## Author

Tiziano Zingales (tiziano.zingales@unipd.it)
