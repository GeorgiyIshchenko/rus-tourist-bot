import json


class City:

    class CityType:
        ZK = "Zolotoe kolco"
        GG = "Gorod Geroi"

    def __init__(self, name, url, _type):
        self.name: str = name
        self.url: str = url
        self._type: City.CityType = _type

    @staticmethod
    async def get_cities_by_name(name: str):
        n = len(name)
        results = list()
        for city in cities_zk + cities_gg:
            if name.lower() == city.name[:n].lower():
                results.append(city)
        return results


cities_zk, cities_gg = list(), list()

with open("cities.json", "r", encoding="utf-8") as f:
    cities = json.load(f)
    for city in cities["cities_zk"]:
        cities_zk.append(City(name=city[0], url=city[1], _type=City.CityType.ZK))
    for city in cities["cities_gg"]:
        cities_gg.append(City(name=city[0], url=city[1], _type=City.CityType.GG))
    cities_zk.sort(key=lambda x: x.name)
