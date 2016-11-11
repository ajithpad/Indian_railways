#Code to use bokeh and gmplot and plot all the stations in India

from bokeh.io import output_file, show
from bokeh.models import (GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool)
from bokeh.models import HoverTool, ResetTool,TapTool
import pickle
from bokeh.charts import Scatter
import matplotlib as mpl

#lat_lon_df = pickle.load(open("data/non_zero_codes.p","rb"))
lat_lon_df = pickle.load(open("data/dep_times_lat_lon.p","rb"))

#lat_lon_df = lat_lon_df.ix[:,['lat','lon']]


map_options = GMapOptions(lat=23.29, lng=78.73,map_type="roadmap", zoom=4)


col_vals = lat_lon_df['num_deps'].values

colors = [
    "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.Blues(mpl.colors.Normalize()(col_vals))
]
lat_lon_df['col_vals'] = colors

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="India"
)

source = ColumnDataSource(lat_lon_df)

#circle = Circle(x="lon", y="lat", size=5, fill_color="blue", fill_alpha=0.7, line_color=None)
circle = Circle(x ='lon', y = 'lat',size = 5, fill_color = 'col_vals')

plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), HoverTool(tooltips = [('name','@name'),('No. of deps/week', '@num_deps'),('Code','@code')]),ResetTool(),TapTool())

output_file("gmap_plot.html")
show(plot)
