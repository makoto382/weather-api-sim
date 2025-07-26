from fastapi import FastAPI, Query
from pydantic import BaseModel  # ←ここを追加！

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Weather!"}

# ----------------------------------------
# 🌦️ GET /weather（クエリパラメータ版）
# ----------------------------------------
@app.get("/weather")
def get_weather(city: str = Query(..., description="都市名を指定")):
    dummy_weather_data = {
        "Tokyo": {"weather": "Sunny", "temperature": "30℃"},
        "Osaka": {"weather": "Cloudy", "temperature": "28℃"},
        "Sapporo": {"weather": "Snow", "temperature": "5℃"},
        "Fukuoka": {"weather": "Rainy", "temperature": "26℃"}
    }
    if city in dummy_weather_data:
        return {"city": city, **dummy_weather_data[city]}
    else:
        return {"city": city, "weather": "Unknown 🌈", "temperature": "N/A"}

# ----------------------------------------
# 📝 POST /weather（天気データの追加）
# ----------------------------------------

# ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ここから下を追記！ ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇

class WeatherData(BaseModel):
    city: str
    weather: str
    temperature: str

weather_db = {}  # 追加データを保存する場所！

@app.post("/weather")
def add_weather(data: WeatherData):
    weather_db[data.city] = {
        "weather": data.weather,
        "temperature": data.temperature
    }
    return {"message": f"{data.city}の天気データを追加したよ！"}


# パスパラメータから都市名を受け取って天気を返す
@app.get("/weather/{city}")
def get_weather_by_path(city: str):
    dummy_weather_data = {
        "Tokyo": {"weather": "Sunny", "temperature": "30℃"},
        "Osaka": {"weather": "Cloudy", "temperature": "28℃"},
        "Sapporo": {"weather": "Snow", "temperature": "5℃"},
        "Fukuoka": {"weather": "Rainy", "temperature": "26℃"},
        "Sapporo": {"weather": "❄️ Snow", "temperature": "5℃"},
    }

    if city in weather_db:
        return {"city": city, **weather_db[city]}
    elif city in dummy_weather_data:
        return {"city": city, **dummy_weather_data[city]}
    else:
        return {"city": city, "weather": "Unknown 🌈", "temperature": "N/A"}
