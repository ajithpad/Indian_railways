# Explore population - number of departures relationships

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool,PanTool, WheelZoomTool, BoxSelectTool
import pickle
import matplotlib as mpl

df = pickle.load(open("data/stat_coo_alt_pop.p","rb"))

df = df[df.lat.values != '']
col_vals = df.lat.values
colors = [
    "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.RdBu(mpl.colors.Normalize()(col_vals))
]

df['col_vals'] = colors

p = figure(title="Population Density vs Number of Departures", x_range = (0, max(df.popden.values)), y_range = (0, max(df.num_deps.values)) )
source = ColumnDataSource(df)
p.circle('popden', 'num_deps', source = source, size = 7, fill_alpha = 0.5, color = 'col_vals')
p.add_tools(HoverTool(tooltips = [('name','@name'),('Code', '@code')]))

output_file("figures/PopVsNum_dep.html", title="Population Density vs Number of Departures")
show(p)