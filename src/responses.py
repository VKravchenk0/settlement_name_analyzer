class SettlementDTO:

    def __init__(self, id: int, name: str, name_en: str, lat: float, lng: float) -> None:
        self.id = id
        self.name = name
        self.name_en = name_en
        self.latitude = lat
        self.longitude = lng
