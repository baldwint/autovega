from collections import OrderedDict
from IPython.display import display, clear_output
import ipywidgets as ipw
import altair as alt

class AutoVega(ipw.VBox):
    def __init__(self, df):
        self.df = df.copy()
        self.chart = alt.Chart(self.df)

        self.chart_types = OrderedDict([
            ('Table', self.on_table),
            ('Scatter', self.on_scatter),
            ('Line', self.on_line),
        ])

        self.toolbar = ipw.ToggleButtons(options=self.chart_types.keys())
        self.toolbar.observe(self.on_chart_type_changed, names='value')

        self.chart_type = 'Table'

        self.encoding = self.guess_encoding()
        self.chart = self.chart.encode(**self.encoding)

        self.dropdowns = []
        for desc,val in self.encoding.items():
            dd = ipw.Dropdown(
                    options=self.df.columns,
                    value=val,
                    description=desc,
                    )
            dd.observe(self.on_encoding_changed, names='value')
            self.dropdowns.append(dd)

        self.encoding_widget = ipw.HBox(self.dropdowns)

        self.content = ipw.Output()
        with self.content:
            display(self._make_mimedict(), raw=True)

        super().__init__([self.toolbar, self.content])

    def _make_mimedict(self):
        # this is essentially what display() does for dataframes,
        # but we might be overriding that
        return {
                "text/plain": repr(self.df),
                "text/html": self.df._repr_html_()
                }

    def guess_encoding(self):
        if len(self.df.columns) < 2:
            raise Exception ('TODO: indexes')
        x,y = self.df.columns[:2]
        return dict(x=x, y=y)

    def on_chart_type_changed(self, change):
        self.chart_type = change['new']
        func = self.chart_types[self.chart_type]
        func()

    def on_encoding_changed(self, change):
        k = change.owner.description
        v = change.new
        self.encoding[k] = v
        self.chart = self.chart.encode(**self.encoding)
        self.redraw_chart()

    def on_table(self):
        with self.content:
            clear_output()
            display(self._make_mimedict(), raw=True)

    def on_scatter(self):
        self.chart = self.chart.mark_point()
        self.redraw_chart()

    def on_line(self):
        self.chart = self.chart.mark_line()
        self.redraw_chart()

    def redraw_chart(self):
        with self.content:
            clear_output()
            display(self.encoding_widget)
            display(self.chart)

def display_dataframe(df):
    av = AutoVega(df)
    display(av)

def register_renderer(func=display_dataframe):
    ip = get_ipython()
    prev_formatter = (ip.display_formatter
            .ipython_display_formatter
            .for_type_by_name(
                'pandas.core.frame',
                'DataFrame',
                func)
            )
    return prev_formatter
