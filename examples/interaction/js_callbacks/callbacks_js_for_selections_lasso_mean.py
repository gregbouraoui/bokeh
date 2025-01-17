from random import random

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure, show

x = [random() for x in range(500)]
y = [random() for y in range(500)]
color = ["navy"] * len(x)

s = ColumnDataSource(data=dict(x=x, y=y, color=color))
p = figure(width=400, height=400, tools="lasso_select", title="Select Here")
p.circle('x', 'y', color='color', size=8, source=s, alpha=0.4)

s2 = ColumnDataSource(data=dict(x=[0, 1], ym=[0.5, 0.5]))
p.line(x='x', y='ym', color="orange", line_width=5, alpha=0.6, source=s2)

s.selected.js_on_change('indices', CustomJS(args=dict(s=s, s2=s2), code="""
    const inds = s.selected.indices;
    const d = s.data;
    let ym = 0

    if (inds.length == 0)
        return;

    for (let i = 0; i < d['color'].length; i++) {
        d['color'][i] = "navy"
    }
    for (let i = 0; i < inds.length; i++) {
        d['color'][inds[i]] = "firebrick"
        ym += d['y'][inds[i]]
    }

    ym /= inds.length
    s2.data['ym'] = [ym, ym]

    s.change.emit();
    s2.change.emit();
"""))

show(p)
