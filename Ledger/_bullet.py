import collections
import math
from plotly import exceptions, optional_imports
import plotly.colors as clrs
from plotly.figure_factory import utils

import plotly
import plotly.graph_objs as go

# vertical bullet chart를 만들기 위한 python script
# bar chart를 이용해 bullet 차트를 만들거임
# range를 설정하고, current 랑 target 설정이 필요함
# 그 다음 색 설정

fig = go.Figure()
fig['layout'].update(
    dict(shapes=[]),
    barmode = "stack", # stack으로 해야 하나로 할 수 있음
    height = 600,
    width = 300,
    showlegend = False
    # annotations = []
    # margin = dict(l = 80)
    )
range_colors = ["rgb(200, 200, 200)", "rgb(245, 245, 245)"]
measure_colors = ["rgb(31, 119, 180)", "rgb(176, 196, 221)"]

for idx in range(len(data.iloc[0]["range"])):
    # range bars: 배경이 되는 range bars
    inter_colors = clrs.n_colors(
        range_colors[0], range_colors[1], len(data.iloc[0]["range"]), "rgb"
    )

    x = [0]
    y = [sorted(data.iloc[0]["range"])[-1 -idx]] # 거꾸로 가는 거
    bar = go.Bar(
        x = x,
        y = y,
        marker = dict(color = inter_colors[-1 - idx]),
        orientation= "v",
        base = 0,
        width = 1,
        # xaxis = "x1"
    )
    fig.add_trace(bar)

# measure bar: current value
for idx in range(len(data.iloc[0]["performance"])):
    inter_colors = clrs.n_colors(
        measure_colors[0], measure_colors[1], len(data.iloc[0]["performance"]),
        "rgb",
    )

    x = [0] # 와 ',' 하나 들어가 있어서 그래프 생성이 안됨
    y = [sorted(data.iloc[0]["performance"])[-1 - idx]]

    bar = go.Bar(
        x = x,
        y = y,
        marker = dict(color = inter_colors[-1 -idx]),
        # name = "yo",
        width = 0.4,
        base = 0

    )
    fig.add_trace(bar)

fig.show()