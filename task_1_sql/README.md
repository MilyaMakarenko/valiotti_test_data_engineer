# Историзация статусов заказов (SCD Type 2)

dpt модель:
 - источник raw.stg_orders (сохраняет только текущее состояние заказа)
   
 ![alt text](image.png)
 
 - сделан слой staging (очистка данных от повторов)
   
 ![alt text](image-1.png)
 
 - сделан снепшот для сохранения истории по дате обновления
   
 ![alt text](image-2.png)
 
 - созданы дата март (материализация табл) как для текущего состояния (источник вью без дубликатов), так и для история (источник снепшот)
   
![alt text](image-4.png)


 Сгенерирована документация
 ![alt text](image-3.png)

 схема DB
 <img width="2426" height="897" alt="image" src="https://github.com/user-attachments/assets/e8dc5069-ea2a-4253-8350-3ad708479aed" />

 Сам проект тоже дб заполнен (семантика)
 <img width="2112" height="1107" alt="image" src="https://github.com/user-attachments/assets/9e8daab8-56f7-48f8-98ba-54ba5f75fba3" />


