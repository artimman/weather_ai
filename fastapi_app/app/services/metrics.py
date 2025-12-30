# FILE: fastapi_app/app/services/metrics.py
def compute_wind_chill(temp_c: float, wind_kph: float) -> float:
    # wind chill formula (approx, for temp <=10°C)
    # temp in °C, wind in km/h
    if temp_c > 10 or wind_kph < 4.8:
        return temp_c
    wc = 13.12 + 0.6215 * temp_c - 11.37 * (wind_kph**0.16) + 0.3965 * temp_c * (wind_kph**0.16)
    return round(wc, 2)

def compute_heat_index(temp_c: float, rh: float) -> float:
    # convert C->F for heat index formula then back
    t_f = temp_c * 9/5 + 32
    hi_f = -42.379 + 2.04901523*t_f + 10.14333127*rh - .22475541*t_f*rh - .00683783*t_f*t_f - .05481717*rh*rh + .00122874*t_f*t_f*rh + .00085282*t_f*rh*rh - .00000199*t_f*t_f*rh*rh
    hi_c = (hi_f - 32) * 5/9
    return round(hi_c, 2)
