from IPython.display import display, clear_output
import ipywidgets as ipw
import traitlets as t
import altair as alt

__version__ = "0.1.dev0"

class ChannelWidget(ipw.HBox):
    """Provides a GUI control for a single Vega channel (X, Y, etc.)
    """
    enabled = t.Bool()
    value = t.Any()

    def __init__(self, channel, options, value=None, enabled=False):
        self.channel = channel
        self.options = options
        self.enabled = enabled
        self.value = value

        self.dropdown = ipw.Dropdown(
                options=self.options,
                value=value,
                description="{}:".format(channel.title()),
                )
        self.dropdown.observe(self.on_value_changed, names='value')

        self.checkbox = ipw.Checkbox(
                value=enabled,
                description='Enabled',
                )
        self.checkbox.observe(self.on_enable_changed, names='value')

        super().__init__([self.dropdown, self.checkbox])

    def on_value_changed(self, change):
        self.value = change['new']

    def on_enable_changed(self, change):
        enabled = change['new']
        if self.dropdown.value is None:
            # make sure this is not null otherwise the plot will fail
            self.dropdown.index = 0  # pick out first option
        self.enabled = enabled

class AutoVega(ipw.VBox):
    def __init__(self, df):
        self.df = df.copy()
        self.chart = alt.Chart(self.df)

        chart_types = ['Table',] + list(self._mark_methods.keys())
        self.toolbar = ipw.ToggleButtons(options=chart_types)
        self.toolbar.observe(self.on_chart_type_changed, names='value')

        initial_encoding = self.guess_encoding()
        self.encoding_widget = self._build_encoding_widget(initial_encoding)

        self.content = ipw.Output()
        with self.content:
            display(self._make_mimedict(), raw=True)

        super().__init__([self.toolbar, self.content])

    def _build_encoding_widget(self, initial_encoding):
        channels = ['x', 'y', 'color']
        self.controls = []
        for channel in channels:
            control = ChannelWidget(channel,
                    self.df.columns,
                    value=initial_encoding.get(channel, None),
                    enabled=(channel in initial_encoding),
                    )
            control.observe(
                    self.on_encoding_changed,
                    names=['value', 'enabled'],
                    )
            self.controls.append(control)

        return ipw.VBox(self.controls)

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

    @property
    def encoding(self):
        return {c.channel: c.value for c in self.controls if c.enabled}

    @property
    def _mark_methods(self):
        mark_method_dict = {
                'Scatter': self.chart.mark_point,
                'Line': self.chart.mark_line,
                'Bar': self.chart.mark_bar,
                }
        return mark_method_dict

    def on_chart_type_changed(self, change):
        """Callback function for the chart type toggle
        """
        new_selection = change['new']
        if new_selection == 'Table':
            self.redraw_table()
        else:
            mark_func = self._mark_methods[new_selection]
            self.chart = mark_func()
            self.redraw_chart()

    def on_encoding_changed(self, change):
        self.redraw_chart()

    def redraw_table(self):
        with self.content:
            clear_output()
            display(self._make_mimedict(), raw=True)

    def redraw_chart(self):
        chart = self.chart.encode(**self.encoding)
        with self.content:
            clear_output()
            display(self.encoding_widget)
            display(chart)

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
