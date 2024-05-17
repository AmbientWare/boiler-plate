import os

from app.db.DynamoDb.database import DynamoDb

selected_db = os.getenv("SELECTED_DB", "DynamoDb")

if selected_db == "DynamoDb":
    app_db = DynamoDb()
else:
    raise NotImplementedError(f"Database {selected_db} not implemented")
