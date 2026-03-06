# import plotly.graph_objects as go
#
# # Data
# betas = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
#          0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# steps = [297, 296, 293, 290, 286, 282, 278, 273, 268, 262,
#          255, 248, 238, 228, 216, 203, 207, 262, 498]
# best_beta = 0.8
# best_steps = 203
# # Create bar chart
# fig = go.Figure(data=[
#     go.Bar(x=betas, y=steps, marker_color='cornflowerblue')
# ])
#
# # Customize layout
# fig.update_layout(
#     title='Beta vs Steps Used for Convergence',
#     xaxis_title='Beta',
#     yaxis_title='Steps Used',
#     xaxis=dict(tickmode='array', tickvals=betas),
#     template='plotly_white'
# )
#
# # Show figure
# fig.show()

import plotly.graph_objects as go

# # Data
# betas = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
#          0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# steps = [336, 363, 331, 343, 321, 333, 316, 305, 322, 311,
#          312, 313, 304, 328, 360, 384, 429, 477, 832]

# # Highlight best beta
# best_beta = 0.65
# best_steps = 304
# colors = ['lightblue' if b != best_beta else 'tomato' for b in betas]

# # Create bar chart
# fig = go.Figure(data=[
#     go.Bar(x=betas, y=steps, marker_color=colors)
# ])

# # Annotate best beta
# fig.add_annotation(x=best_beta, y=best_steps,
#                    text=f"Best β = {best_beta}<br>Steps = {best_steps}",
#                    showarrow=True, arrowhead=2, ax=0, ay=-40, bgcolor='white')

# # Layout customization
# fig.update_layout(
#     title='US Airlines: Beta vs Steps Used for Convergence',
#     xaxis_title='Beta',
#     yaxis_title='Steps Used',
#     xaxis=dict(tickmode='array', tickvals=betas),
#     template='plotly_white'
# )

# # Show plot
# fig.show()

# import plotly.graph_objects as go
#
# # Data
# betas = [
#     0.05,
#     0.1,
#     0.15,
#     0.2,
#     0.25,
#     0.3,
#     0.35,
#     0.4,
#     0.45,
#     0.5,
#     0.55,
#     0.6,
#     0.65,
#     0.7,
#     0.75,
#     0.8,
#     0.85,
#     0.9,
#     0.95,
# ]
neurons_8 = [
1084,
1056,
1022,
1017,
1007,
970,
944,
930,
897,
865,
826,
816,
783,
728,
667,
639,
594,
]
#
# random = [
#     299,
#     288,
#     276,
#     298,
#     283,
#     270,
#     287,
#     286,
#     233,
#     269,
#     254,
#     241,
#     254,
#     270,
#     397,
#     412,
#     372,
#     404,
#     528,
#     847
# ]

celegans = [
227,
229,
229,
232,
233,
235,
237,
238,
242,
251,
259,
253,
269,
292,
6292,
1821,
2828,
]

# email_eu_core = [
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
#     10,
# ]

neurons_1 = [
225,
221,
214,
210,
205,
197,
191,
185,
178,
171,
165,
161,
169,
184,
204,
223,
253,
]

neurons_2 = [
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
]
#
# random_2 = [
#     74,
#     73,
#     71,
#     69,
#     68,
#     66,
#     64,
#     64,
#     63,
#     62,
#     61,
#     63,
#     67,
#     72,
#     80,
#     91,
#     113,
#     147,
#     220,
#     439,
# ]

jazz = [
166,
165,
166,
165,
163,
162,
163,
162,
161,
164,
164,
168,
174,
184,
196,
214,
235,
]

les_miserables = [
17,
18,
18,
18,
19,
19,
19,
20,
20,
22,
22,
23,
26,
26,
26,
31,
34,
]

us_airlines = [
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
6894,
694,
951,
1408    ,
]

us_migration = [
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
10000,
]


betas = [
    0.0, 0.05, 0.1, 0.15, 0.2,
    0.25, 0.3, 0.35, 0.4, 0.45,
    0.5, 0.55, 0.6, 0.65, 0.7,
    0.75, 0.8
]

# Dataset lists
datasets = [neurons_8, us_airlines, celegans, us_migration, neurons_1, neurons_2, jazz, les_miserables]

# Compute total steps per beta
steps = [sum(values) for values in zip(*datasets)]
# Determine best beta (minimum steps)
min_steps = min(steps)
best_index = steps.index(min_steps)
best_beta = betas[best_index]
best_steps = steps[best_index]

colors = ["lightblue" if b != best_beta else "tomato" for b in betas]

# Create bar chart
fig = go.Figure(data=[go.Bar(x=betas, y=steps, marker_color=colors)])

# Highlight best beta with annotation
fig.add_annotation(
    x=best_beta,
    y=best_steps,
    text=f"Best β = {best_beta}<br>Steps = {best_steps}",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="white",
)

# Layout settings
fig.update_layout(
    title="Total Steps per Beta Across Datasets",
    xaxis_title="Beta",
    yaxis_title="Steps Used",
    xaxis=dict(tickmode="array", tickvals=betas),
    template="plotly_white",
)

# Show plot
fig.show()



#
# import plotly.graph_objs as go
#
# # Original data
# datasets = [
#     "US Airlines", "US Migration", "EuroSiS", "Jazz",
#     "C. Elegans", "Email EU", "BB1", "BB2", "BB8"
# ]
# edges = [2101, 9780, 7586, 2742, 2148, 25571, 240, 1790, 1128]
# mseb_times = [33556, 913540, 683065, 49685, 42490, 11381598, 736, 23784, 10576]
# emseb_times = [26269, 687992, 437925, 38638, 27538, 623872, 590, 18344, 8375]
#
# # Zip and sort by number of edges
# data = list(zip(edges, mseb_times, emseb_times, datasets))
# data.sort()  # Sorts by the first element: edges
#
# # Unzip sorted data
# sorted_edges, sorted_mseb, sorted_emseb, sorted_labels = zip(*data)
#
# # Create the plot
# fig = go.Figure()
#
# fig.add_trace(go.Scatter(
#     x=sorted_edges, y=sorted_mseb,
#     mode='lines+markers+text',
#     name='MSEB',
#     # text=sorted_labels,
#     textposition='top center',
#     line=dict(color='blue'),
#     marker=dict(symbol='circle', size=8)
# ))
#
# fig.add_trace(go.Scatter(
#     x=sorted_edges, y=sorted_emseb,
#     mode='lines+markers+text',
#     name='EMSEB',
#     # text=sorted_labels,
#     textposition='bottom center',
#     line=dict(color='green'),
#     marker=dict(symbol='square', size=8)
# ))
#
# fig.update_layout(
#     title="Runtime vs Number of Edges (MSEB vs EMSEB)",
#     xaxis_title="Number of Edges",
#     yaxis_title="Runtime (ms)",
#     legend_title="Algorithm",
#     template="plotly_white",
#     hovermode="closest"
# )
#
# fig.show()
