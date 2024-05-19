from django.db import connection
from django import template
from datetime import datetime, timedelta

def query_result(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description is None:
            return []  # or return None, depending on how you want to handle this case
        
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        data = []
        for row in results:
            data.append(dict(zip(columns, row))) 
        return data
    


