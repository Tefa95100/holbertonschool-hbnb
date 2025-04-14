from app import create_app
from app.services.facade import HBnBFacade

app = create_app()
facade = HBnBFacade()

def create_admin_user():
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "admin123",
        "is_admin": True
    }
    existing_user = facade.user_repo.get_user_by_email(admin_data["email"])
    if existing_user:
        print(f"Admin user already exists: {existing_user.email}")
    else:
        new_admin = facade.create_user(admin_data)
        print(f"Admin user created: {new_admin.email}")

if __name__ == "__main__":
    with app.app_context():  # Ensure application context is active
        create_admin_user()
    app.run(debug=True)
