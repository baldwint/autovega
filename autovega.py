from IPython.core.display import display
from IPython.display import clear_output
import ipywidgets as ipw
import altair as alt

class AutoVega(ipw.VBox):
    def __init__(self, df):
        self.df = df.copy()

        buts = [
            ('Table', self.on_table),
            ('Scatter', self.on_scatter),
            ('Line', self.on_line),
        ]

        self.buttons = []
        for desc,callback in buts:
            but = ipw.Button(description=desc)
            but.on_click(callback)
            self.buttons.append(but)

        self.toolbar = ipw.HBox(self.buttons)

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

    def on_table(self, button):
        with self.content:
            clear_output()
            print('you picked Table')
            display(self._make_mimedict(), raw=True)

    def on_scatter(self, button):
        c = alt.Chart(self.df).mark_point().encode(x='ha', y='lo')
        with self.content:
            clear_output()
            print('you picked Scatter')
            display(c)

    def on_line(self, button):
        c = alt.Chart(self.df).mark_line().encode(x='ha', y='lo')
        with self.content:
            clear_output()
            print('you picked Line')
            display(c)

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
