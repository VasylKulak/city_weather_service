from pydantic import BaseModel, field_validator


class BaseCitySchema(BaseModel):
    city: str


class CityWeatherRequest(BaseCitySchema):
    @field_validator("city")
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().lower().replace(" ", "")


class CityWeatherLog(BaseCitySchema):
    created_at: int
    storage_path: str


class CityWeatherResponse(BaseCitySchema):
    country: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    clouds: int
