from locust import HttpUser, task
from tests.test_load.utils import generate_user_info


class QuickstartUser(HttpUser):
    @task
    def full_user_path(self):
        user_info = generate_user_info()
        self.client.get(url="/session")
        self.client.post(
            url="/register",
            json={
                "username": user_info["username"],
                "email": user_info["email"],
                "password": user_info["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        self.client.post(
            url="/login",
            json={
                "username": user_info["username"],
                "password": user_info["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        self.client.get(url="/user")
        self.client.patch(
            url="/user",
            json={
                "password": user_info["new_password"]
            },
            headers={"Content-Type": "application/json"}
        )
        self.client.post(url="/logout")
        self.client.post(
            url="/login",
            json={
                "username": user_info["username"],
                "password": user_info["new_password"]
            },
            headers={"Content-Type": "application/json"}
        )
        self.client.delete(url="/user")
