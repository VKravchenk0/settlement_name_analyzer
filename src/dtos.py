class MissingCoordinatesSettlementDTO(object):

    def __init__(self, id: int, name: str, lat: str = "", lon: str = "") -> None:
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
