# GDPR обработчик персональных данных

## Задача
Обработать CSV файл с персональными данными (email) для соответствия GDPR.  
Зашифровать email с возможностью обратной расшифровки. Сохранить результат.

## Решение

<img width="700" height="208" alt="image" src="https://github.com/user-attachments/assets/08ba3daf-1ebb-4a3e-b6ab-bccf8bdc2cec" />

<img width="700" height="174" alt="image" src="https://github.com/user-attachments/assets/dbb9d295-f66a-4039-ac7d-727e538c2d1f" />



### Файлы
- `processor.py` - основная функция обработки
- `requirements.txt` - зависимости
- `test_data.csv` - тестовые данные 
- `test_data_encrypted.csv` - тестовый результат после шифрования

### Как работает
1. Читает CSV из S3 (или локального файла)
2. Шифрует колонку email через Fernet (симметричное шифрование)
3. Сохраняет результат в другой S3 бакет (или локальный файл)
4. Можно расшифровать при необходимости (обратимость)

### Зависимости
- Python 3.9+
- boto3 (для доступа к S3)
- cryptography (для шифрования Fernet)

### Переменные окружения
- `FERNET_KEY` - ключ шифрования 
- `OUTPUT_BUCKET` - куда сохранять результат
- `BATCH_SIZE` - строк в одном батче (по умрлчанию 5тыс)

