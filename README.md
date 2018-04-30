# autovega

`autovega` is an IPython/Jupyter notebook widget for quick and dirty visualization of Pandas dataframes using Vega and Altair.

## Usage

Import autovega and call `register_renderer` at the top of your notebook.

```python
import autovega
autovega.register_renderer()
```

Now, whenever Jupyter displays a dataframe, it will also render a GUI for choosing one of several plot types and encodings.

## Installation

Follow the instructions for installing and configuring `altair` and `vega3`. Then install autovega:

```bash
pip install autovega
```

