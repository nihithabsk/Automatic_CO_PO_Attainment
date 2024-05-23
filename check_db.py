# In check_db.py

from app import app, db
from app.models import CalculationResult

app.app_context().push()

# Query all records from the CalculationResult table
results = CalculationResult.query.all()

# Print the records
for result in results:
    print(result.id, result.average, result.level)
