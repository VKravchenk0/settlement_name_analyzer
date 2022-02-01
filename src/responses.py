class SettlementDTO:

    def __init__(self, id: int, name: str, lat: float, lng: float) -> None:
        self.id = id
        self.name = name
        self.latitude = lat
        self.longitude = lng
