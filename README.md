
# About the project ***`data_analysis_app_weatherAPI`***

[![app Weather Analysis CI/CD](https://github.com/nikfilonenko/data_analysis_app_weatherAPI/actions/workflows/app_weather_analysis.yml/badge.svg)](https://github.com/nikfilonenko/data_analysis_app_weatherAPI/actions/workflows/app_weather_analysis.yml)


## 🌐 Ссылка на развернутое приложение в Streamlit Cloud: [Здесь](https://dataanalysisappweatherapi-kjje8rplqtbrfqz3rpzqcu.streamlit.app/)

`https://dataanalysisappweatherapi-kjje8rplqtbrfqz3rpzqcu.streamlit.app/`

<br>

## 📊 Ноутбук с дополнительными исследованиями: [Здесь](app/notebooks/data_analysis.ipynb)

`app/notebooks/data_analysis.ipynb`


-----

### Содержание

1. [Описание проекта](#01)
2. [Исследование](#02)
   - [Анализ исторических данных](#021)
   - [Исследование распараллеливания анализа данных](#022)
   - [Проведение эксперимента с синхронным и асинхронным способом запроса к API](#023)
4. [Streamlit приложение](#03)
   - [📁 Загрузка данных](#031)
   - [📊 Анализ данных](#032)
   - [📈 Визуализация](#033)
   - [🌡️ Текущая температура OpenWeatherAPI](#034)
5. [Развертывание приложения](#04)
6. [Демонстрация работы Streamlit приложения](#05)

### Описание проекта <a name="01"></a>

### Исследование <a name="02"></a>

#### 1. Анализ исторических данных <a name="021"></a>

#### 2. Исследование распараллеливания анализа данных <a name="022"></a>

![img_4.png](assets/img_4.png)

![img_1.png](assets/img_1.png)

#### 3. Проведение эксперимента с синхронным и асинхронным способом запроса к API <a name="023"></a>

![img_2.png](assets/img_2.png)

![img_3.png](assets/img_3.png)


- выполнение асинхронных запросов к API (более одного города за раз):


```python
Время выполнения асинхронных запросов: 0.25 секунд

Результаты запросов:
Moscow: -3.66°C
Berlin: 8.95°C
Paris: 6.17°C
Tokyo: 8.09°C
```

- выполнение синхронных запросов к API (более одного города за раз):

```python
Время выполнения синхронных запросов: 0.92 секунд

Результаты запросов:
Moscow: -3.66°C
Berlin: 8.74°C
Paris: 6.17°C
Tokyo: 8.09°C

Синхронные запросы заняли 0.92 секунд, асинхронные — 0.25 секунд.
Асинхронные запросы быстрее.
```

### Streamlit приложение <a name="03"></a>

#### 1. 📁 Загрузка данных <a name="031"></a>

#### 2. 📊 Анализ данных <a name="032"></a>

#### 3. 📈 Визуализация <a name="033"></a>

#### 4. 🌡️ Текущая температура OpenWeatherAPI <a name="034"></a>


### Развертывание приложения <a name="04"></a>

### Демонстрация работы Streamlit приложения <a name="05"></a>



https://github.com/user-attachments/assets/2230290c-1277-4404-996e-6215e245851a

