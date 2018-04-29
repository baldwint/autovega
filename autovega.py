from IPython.display import display, clear_output
import ipywidgets as ipw
import altair as alt

class AutoVega(ipw.VBox):
    def __init__(self, df):
        self.df = df.copy()
        self.chart = alt.Chart(self.df)

        chart_types = ['Table',] + list(self._mark_methods.keys())
        self.toolbar = ipw.ToggleButtons(options=chart_types)
        self.toolbar.observe(self.on_chart_type_changed, names='value')

        self.encoding = self.guess_encoding()
        self.encoding_widget = self._build_encoding_widget()

        self.content = ipw.Output()
        with self.content:
            display(self._make_mimedict(), raw=True)

        super().__init__([self.toolbar, self.content])

    def _build_encoding_widget(self):
        channels = ['x', 'y', 'color']
        controls = {}
        self.dropdowns = {} # dropdown lookup, so we can fetch the
                            # channel value when reenabling a channel.
                            # TODO: get rid of this somehow
        self.checkboxes = {} # ditto
        for channel in channels:
            val = self.encoding.get(channel, None)
            dd = ipw.Dropdown(
                    options=self.df.columns,
                    value=val,
                    description="{}:".format(channel.title()),
                    )
            dd.channel = channel  # attach attribute for callback
            dd.observe(self.on_encoding_changed, names='value')

            cb = ipw.Checkbox(
                    value=channel in self.encoding,
                    description='Enabled',
                    )
            cb.channel = channel  # attach attribute for callback
            cb.observe(self.on_encoding_enabled, names='value')

            controls[channel] = ipw.HBox([dd,cb])
            self.dropdowns[channel] = dd
            self.checkboxes[channel] = cb

        return ipw.VBox([controls[c] for c in channels])

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
        """Callback function for the channel dropdowns
        """
        channel = change.owner.channel
        value = change.new
        checkbox = self.checkboxes[channel]
        if checkbox.value:  # if this channel is enabled
            self.encoding[channel] = value
            self.redraw_chart()

    def on_encoding_enabled(self, change):
        """Callback function for the 'Enabled' checkbox
        """
        channel = change.owner.channel
        if change.new is False:
            self.encoding.pop(channel)
        else:
            dropdown = self.dropdowns[channel]
            self.encoding[channel] = dropdown.value
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
