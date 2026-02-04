# python-backend

Mini project này có cấu trúc là
│ .env
│ main.py
│ README.md
│
├───api
│ user_router.py
│
├───config
│ settings.py
│  
│  
│  
│
├───database
│ mysql_conn.py
│
├───domain
│ │ exceptions.py
│ │
│ └───entities
│ user.py
│  
│  
│  
│
├───factories
│ user_factory.py
│
├───repositories
│ user_repository.py
│ user_repository_fake.py
│ user_repository_mysql.py
│
├───schemas
│ user_schema.py
│
└───usecases
user_usecase.py

- settings.py phục vụ việc lấy cấu hình env ra
- mysql_conn sẽ import class DatabaseConfig để phục vụ việc kết nối db
- user_repository là interface nhưng do thuộc phạm vi mini project nên mới để cùng folder repositories (nếu trong trường hợp mở rộng hoặc dự án to hơn thì sẽ ở trong folder domain/interfaces)
- user_repository_fake nhằm phục vụ khi đang trong môi trường test
- user_factory phục vụ việc luân chuyển giữa kết nối db và test
