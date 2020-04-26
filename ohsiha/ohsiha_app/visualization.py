from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from datetime import datetime
from dateutil import parser
from .models import Choice
from bokeh.models import ColumnDataSource

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

    plot.vbar(x=stript_labels, top=data, width=0.9, line_color = '#96031A', fill_color = '#FF6978')

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
        data.append(i)

    labels = e.bar_labels.split(',')
    barlabels = []

    for label in labels:
        datetime_obj = parser.parse(label)
        barlabels.append(datetime_obj)


    plot = figure(title = 'Tartunnat kumulatiivisesti', x_axis_label = 'päivä',
            y_axis_label = "Määrä", plot_width = 600, plot_height = 400 , x_axis_type='datetime')

    plot.line(barlabels, data, line_width = 2, line_color = '#96031A')        


    plot.y_range.start = 0
    plot.xaxis.major_label_orientation = 1
    script, div = components(plot)

    return script, div

def make_user_data_linegraph(all_answers):
    data_dict = {}

    for answer in all_answers:
        choice = Choice.objects.get(id = answer.choise_id)
        if answer.date in data_dict:
            old_val = data_dict[answer.date]
            new_val = (old_val + choice.category)
            data_dict.update({answer.date : new_val})
        else:
            data_dict.update( {answer.date : choice.category} )

    barlabels = list()
    data = list()
    for i in data_dict.keys():
        date = datetime(i.year, i.month, i.day)
        barlabels.append(date)
        print(date)

    for i in data_dict.values():
        data.append(i)
        print(i)

    #barlabels = list(range(len(data)))

    plot = figure(title = 'Vastausten keskiarvo', x_axis_label = 'päivä',
            y_axis_label = "Kategoria", plot_width = 600, plot_height = 400 ,x_axis_type='datetime')           

    source = ColumnDataSource(data=dict(x=barlabels, y=data))

    plot.line(x='x', y='y', source = source, line_width = 2, line_color = '#96031A')        

    plot.y_range.start = 0
    plot.xaxis.major_label_orientation = 1
    script, div = components(plot)

    return script, div    



