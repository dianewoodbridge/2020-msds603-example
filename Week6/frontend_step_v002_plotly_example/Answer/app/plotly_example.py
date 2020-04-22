import plotly
from plotly.graph_objs import Layout, Scattermapbox

from statistics import mean


def plotly_map(locations):
    mapbox_access_token = 'pk.eyJ1Ijoic3VodHdpbnMiLCJhIjoi' +\
                        'Y2pnNGJvbXRhMGpoNDJwcWRva3JieWgwcCJ9' +\
                        '.cmsuwG65XkGUh2pv07nIVg'

    data = [
        Scattermapbox(
            lat=[location.latitude for location in locations],
            lon=[location.longitude for location in locations],
            text=[location.name for location in locations],
            mode='markers',
        )]

    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=mean([location.latitude for location in locations]),
                lon=mean([location.longitude for location in locations])
            ),
            pitch=100,
            zoom=10
        ),
    )

    fig = dict(data=data, layout=layout)
    output = plotly.offline.plot(fig, include_plotlyjs=False,
                                 output_type='div')
    return(output)


if __name__=="__main__":
    plotly_map()