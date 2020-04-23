from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from datetime import datetime
from dateutil import parser

def make_barchart(e):
    data_str = e.data.split(",")
    data = []
    for elem in data_str:
        data.append(int(elem))
    
    labels = e.bar_labels.split(',')
    stript_labels =[]

    for label in labels:
        stript_labels.append(label[8:10] + "/" + label[5:7]) 

    plot = figure(x_range = stript_labels, plot_height=400, title="Tartunnat päivittäin", tools="")

    plot.vbar(x=stript_labels, top=data, width=0.9)

    plot.y_range.start = 0
    plot.xaxis.major_label_orientation = 1
    script, div = components(plot)

    return script, div

def make_linegraph(e):
    data_str = e.data.split(",")
    data = []
    i = 0
    for elem in data_str:
        i = i + int(elem)
        print(i)
        data.append(i)

    labels = e.bar_labels.split(',')
    barlabels = []

    for label in labels:
        datetime_obj = parser.parse(label)
        barlabels.append(datetime_obj)


    plot = figure(title = 'Tartunnat kumulatiivisesti', x_axis_label = 'päivä',
            y_axis_label = "Määrä", plot_width = 600, plot_height = 400 , x_axis_type='datetime')

    plot.line(barlabels, data, line_width = 2)        


    plot.y_range.start = 0
    plot.xaxis.major_label_orientation = 1
    script, div = components(plot)

    return script, div
