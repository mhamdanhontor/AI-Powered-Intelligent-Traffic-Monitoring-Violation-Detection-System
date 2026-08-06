from app.database import Base
from app.database import engine

import app.models.violation_model

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")