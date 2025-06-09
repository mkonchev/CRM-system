from locust import HttpUser, task, between
import random
import string


class OrderLoadTest(HttpUser):
    wait_time = between(0.5, 2)

    def on_start(self):
        self.created_orders = []
        self.first_names = ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей",
                            "Андрей", "Михаил"]
        self.last_names = ["Иванов", "Петров", "Сидоров", "Смирнов",
                           "Кузнецов", "Попов", "Васильев"]
        self.middle_names = ["Иванович", "Петрович", "Алексеевич",
                             "Дмитриевич", "Сергеевич"]
        self.car_brands = ["Toyota", "Honda", "BMW", "Mercedes", "Audi",
                           "Volkswagen"]
        self.car_models = ["Camry", "Accord", "X5", "E-Class", "A4", "Passat"]

    def generate_random_email(self):
        domains = ["gmail.com", "yahoo.com", "mail.ru", "yandex.ru"]
        name = ''.join(random.choices(string.ascii_lowercase,
                                      k=random.randint(5, 10)))
        return f"{name}@{random.choice(domains)}"

    def generate_random_phone(self):
        return f"+79{random.randint(10000000, 99999999)}"

    def generate_random_password(self):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=random.randint(8, 12)))

    @task(2)
    def create_user(self):
        data = {
            'email': self.generate_random_email(),
            'first_name': random.choice(self.first_names),
            'last_name': random.choice(self.last_names),
            'phone_number': self.generate_random_phone(),
            'password': self.generate_random_password(),
        }
        response = self.client.post(
            "/api/user/create", 
            json=data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            try:
                response_data = response.json()
                if "id" in response_data:
                    self.created_orders.append(response_data["id"])
                    print(f"Created user with ID: {response_data['id']}")
            except ValueError:
                print("Failed to parse JSON response")

    @task(1)
    def get_user_list(self):
        self.client.get("/api/user/")

    @task(1)
    def get_user_by_id(self):
        if self.created_orders:
            user_id = random.choice(self.created_orders)
            self.client.get(f"/api/user/{user_id}")

    @task(1)
    def update_user(self):
        if self.created_orders:
            user_id = random.choice(self.created_orders)
            data = {
                'last_name': random.choice(self.last_names),
                'first_name': random.choice(self.first_names),
                'phone_number': self.generate_random_phone(),
            }
            self.client.patch(
                f"/api/user/{user_id}/update", 
                json=data,
                headers={"Content-Type": "application/json"}
            )

    @task(1)
    def delete_user(self):
        if self.created_orders:
            user_id = self.created_orders.pop(0)
            self.client.delete(f"/api/user/{user_id}/delete")
