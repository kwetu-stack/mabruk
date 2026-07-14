from app import app
from models.user import User

with app.app_context():

    print("\n=== USERS ===\n")

    users = User.query.all()

    for u in users:
        print(
            f"{u.username} | {u.role} | Active={u.active}"
        )

    print("\n=== ADMIN PASSWORD TEST ===\n")

    admin = User.query.filter_by(username="admin").first()

    if admin:

        print("admin123 :", admin.check_password("admin123"))
        print("admin1234:", admin.check_password("admin1234"))

    else:

        print("Admin user not found.")