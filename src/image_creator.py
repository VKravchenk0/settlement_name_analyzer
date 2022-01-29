import geopandas as gpd
from shapely.geometry import Point
from typing import List


def plot_settlements(settlements: List):
    print("plot settlements: " + str(len(settlements)))
    print(settlements)
    points = []
    for s in settlements:
        points.append(Point(s.lng, s.lat))
    print("printing points")
    print(points)
    return create_geo_image(points)


def create_geo_image(points: List):
    crs = {'init': 'EPSG:4326'}

    geo_df = gpd.GeoDataFrame(geometry=points, crs=crs)

    df = gpd.read_file("./resources/geopandas_shapes/UKR_adm1.shp")
    print(df.head())

    ax = df.plot(color="orange")
    ax.set_axis_off()

    geo_df.plot(ax=ax)

    return ax.get_figure()