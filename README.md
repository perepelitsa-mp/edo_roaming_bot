# Roaming Bot

## Описание
Roaming Bot — это автоматизированный скрипт, который взаимодействует с веб-интерфейсом Диадока для отправки заявок на роуминг. Скрипт использует Selenium для автоматизации действий в браузере и отправляет результаты запросов на указанный сервер.

## Description
Roaming Bot is an automated script that interacts with the Diadoc web interface to submit roaming requests. The script uses Selenium to automate browser actions and sends the results of the requests to a specified server.

## Требования
- Python 3.9
- Selenium
- ChromeDriver
- FFmpeg (для записи видео)
- Другие зависимости, указанные в `requirements.txt`

## Requirements
- Python 3.9
- Selenium
- ChromeDriver
- FFmpeg (for video recording)
- Other dependencies listed in `requirements.txt`

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Убедитесь, что ChromeDriver и FFmpeg установлены и доступны в системе.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure that ChromeDriver and FFmpeg are installed and available in the system.

## Настройка
1. Создайте файл `settings.json` в корневой директории проекта со следующими параметрами:
   ```json
   {
     "ID": "your_id",
     "inn_org": "your_inn_org",
     "email_dlya_svyza": "your_email",
     "inn_contr": "your_inn_contr",
     "name_contr": "your_name_contr",
     "oper": "your_oper"
   }
   ```
2. Замените конфиденциальные данные (пути, логины, пароли, URL и т.д.) в файле `main.py` на соответствующие значения.

## Configuration
1. Create a `settings.json` file in the root directory of the project with the following parameters:
   ```json
   {
     "ID": "your_id",
     "inn_org": "your_inn_org",
     "email_dlya_svyza": "your_email",
     "inn_contr": "your_inn_contr",
     "name_contr": "your_name_contr",
     "oper": "your_oper"
   }
   ```
2. Replace confidential data (paths, logins, passwords, URLs, etc.) in the `main.py` file with the corresponding values.

## Запуск
Для запуска скрипта выполните команду:
```bash
python main.py
```

## Running
To run the script, execute the command:
```bash
python main.py
```

## Примеры использования
Скрипт автоматически заполняет форму на сайте Диадока, отправляет заявку и записывает результат в лог-файл. Результаты также отправляются на указанный сервер.

## Usage Examples
The script automatically fills out the form on the Diadoc website, submits the request, and logs the result. The results are also sent to the specified server.

## Логирование
Логи сохраняются в файл `roaming.log` в корневой директории проекта.

## Logging
Logs are saved to the `roaming.log` file in the root directory of the project.
