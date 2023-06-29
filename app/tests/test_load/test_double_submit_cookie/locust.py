from locust import HttpUser, task
from tests.test_load.utils import generate_user_info


class QuickstartUser(HttpUser):
    @task
    def full_user_path(self):
        user_info = generate_user_info()
        response = self.client.get(url="/session")
        response = self.client.post(
            url="/register",
            json={
                "username": user_info["username"],
                "email": user_info["email"],
                "password": user_info["password"],
                "csrf_token": response.cookies["csrf_token"]
            },
            headers={"Content-Type": "application/json"},
        )
        self.client.post(
            url="/login",
            json={
                "username": user_info["username"],
                "password": user_info["password"],
                "csrf_token": response.cookies["csrf_token"]
            },
            headers={"Content-Type": "application/json"}
        )
        response = self.client.get(url="/user")
        response = self.client.patch(
            url="/user",
            json={
                "password": user_info["new_password"],
                "csrf_token": response.cookies["csrf_token"]
            },
            headers={"Content-Type": "application/json"}
        )
        response = self.client.post(
            url="/logout",
            json={"csrf_token": response.cookies["csrf_token"]}
        )
        response = self.client.post(
            url="/login",
            json={
                "username": user_info["username"],
                "password": user_info["new_password"],
                "csrf_token": response.cookies["csrf_token"]
            },
            headers={"Content-Type": "application/json"}
        )
        self.client.delete(
            url="/user",
            json={"csrf_token": response.cookies["csrf_token"]}
        )
