""" Demonstration of how to register event callbacks using an adaptation of
the color_scatter example from the Bokeh gallery

"""
import numpy as np

from bokeh import events
from bokeh.layouts import column, row
from bokeh.models import Button, CustomJS, Div
from bokeh.plotting import figure, show


def display_event(div, attributes=[], style = 'float:left;clear:left;font_size=13px'):
    "Build a suitable CustomJS to display the current event in the div model."
    return CustomJS(args=dict(div=div), code="""
        const attrs = %s;
        const args = [];
        for (let i = 0; i<attrs.length; i++) {
            args.push(attrs[i] + '=' + Number(cb_obj[attrs[i]]).toFixed(2));
        }
        const line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
        const text = div.text.concat(line);
        const lines = text.split("\\n")
        if (lines.length > 35)
            lines.shift();
        div.text = lines.join("\\n");
    """ % (attributes, style))

x = np.random.random(size=4000) * 100
y = np.random.random(size=4000) * 100
radii = np.random.random(size=4000) * 1.5
colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)]

p = figure(tools="pan,wheel_zoom,zoom_in,zoom_out,reset")
p.scatter(x, y, radius=np.random.random(size=4000) * 1.5,
          fill_color=colors, fill_alpha=0.6, line_color=None)

div = Div(width=400, height=p.height, height_policy="fixed")
button = Button(label="Button", button_type="success")
layout = column(button, row(p, div))

# events with no attributes
button.js_on_event(events.ButtonClick, display_event(div)) # Button click
p.js_on_event(events.LODStart, display_event(div))         # Start of LOD display
p.js_on_event(events.LODEnd, display_event(div))           # End of LOD display

# events with attributes
point_attributes = ['x', 'y', 'sx', 'sy']                  # Point events
wheel_attributes = point_attributes + ['delta']            # Mouse wheel event
pan_attributes = point_attributes + ['delta_x', 'delta_y'] # Pan event
pinch_attributes = point_attributes + ['scale']            # Pinch event

point_events = [
    events.Tap, events.DoubleTap, events.Press, events.PressUp,
    events.MouseMove, events.MouseEnter, events.MouseLeave,
    events.PanStart, events.PanEnd, events.PinchStart, events.PinchEnd,
]

for event in point_events:
    p.js_on_event(event, display_event(div, attributes=point_attributes))

p.js_on_event(events.MouseWheel, display_event(div, attributes=wheel_attributes))
p.js_on_event(events.Pan,        display_event(div, attributes=pan_attributes))
p.js_on_event(events.Pinch,      display_event(div, attributes=pinch_attributes))

show(layout)
