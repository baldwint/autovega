# autovega

`autovega` is an IPython/Jupyter notebook widget for quick visualization of Pandas dataframes using [Vega](https://vega.github.io/) and [Altair](https://altair-viz.github.io/).

## Usage

Import autovega and call `register_renderer` at the top of your notebook.

```python
import autovega
autovega.register_renderer()
```

Now, whenever Jupyter displays a dataframe, it will also render a GUI for choosing one of several plot types and encodings.

Alternatively, to use the widget selectively (without registering it as the default dataframe renderer in Jupyter), use the `display_dataframe` function to wrap your dataframes.

```python
autovega.display_dataframe(df)
```

## Installation

Follow [Altair's instructions](https://altair-viz.github.io/getting_started/installation.html) for installing and configuring `altair` and `vega3`. Then install autovega:

```bash
pip install autovega
```

Or, for the development version:

```bash
pip install -e git+https://github.com/baldwint/autovega.git#egg=autovega
```

