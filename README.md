# Учебный проект по управление потоком операций с применением Apache Airflow и MLflow.<br>
Данные собираются с сайта 'https://yandex.ru/pogoda/month/{self.MONTHS[month]}?lat=56.829472&lon=60.532538&via=ms' (в зависимости от текущего месяца),<br>
обрабатываются и передаются в модель SARIMAX для обучения и предсказания погоды. Airflow используется для автоматизации операций, а MLFlow для мониторинга процессов.
![Иллюстрация к проекту 1](https://github.com/Deszher/weather_predict/raw/main/image/image1.png)
![Иллюстрация к проекту 2](https://github.com/Deszher/weather_predict/raw/main/image/image2.png)
