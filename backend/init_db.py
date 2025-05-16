from app import app, db
from models.user import User
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(
        full_name="Aswin R K",
        email="aswinrk.radhakrishnan@gmail.com",
        password="anythingsecure",  # Plaintext for now
        age=20,
        working_status="Student",
        created_at=datetime.now()
    )
    db.session.add(user)
    db.session.commit()

    print("✅ Database initialized and sample user added!")
