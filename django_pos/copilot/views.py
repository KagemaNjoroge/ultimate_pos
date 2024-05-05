import json
from django.http import HttpRequest, JsonResponse
import requests
from django.conf import settings
from django.views.decorators.http import require_http_methods
from groq import Groq
from dotenv import load_dotenv
import os
from sales.models import Sale
from django.db import connection

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


statement = """

        SELECT
    'CREATE TABLE ' || table_name || ' (' ||
    array_to_string(array_agg(column_definition), ', ') ||
    CASE
        WHEN array_agg(is_updatable)::text != '{"YES"}' THEN
            ', CONSTRAINT ' || table_name || '_pk PRIMARY KEY (' || array_to_string(array_agg(column_name), ', ') || ')'
        ELSE
            ''
    END ||
    CASE
        WHEN foreign_key_column IS NOT NULL THEN
            ', CONSTRAINT ' || table_name || '_fk FOREIGN KEY (' || foreign_key_column || ') REFERENCES ' || foreign_table || '(' || referenced_column || ')'
        ELSE
            ''
    END ||
    ')'
FROM (
    SELECT
        c.table_name,
        c.column_name,
        c.data_type ||
        CASE
            WHEN c.character_maximum_length IS NOT NULL THEN '(' || c.character_maximum_length || ')'
            ELSE ''
        END ||
        CASE
            WHEN c.is_nullable = 'NO' THEN ' NOT NULL'
            ELSE ''
        END ||
        CASE
            WHEN c.column_default IS NOT NULL THEN ' DEFAULT ' || c.column_default
            ELSE ''
        END AS column_definition,
        c.is_updatable,
        ccu.column_name AS foreign_key_column,
        ccu.table_name AS foreign_table,
        ccu.column_name AS referenced_column
    FROM
        information_schema.columns c
    LEFT JOIN
        information_schema.table_constraints tc ON c.table_name = tc.table_name
    LEFT JOIN
        information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
    WHERE
        c.table_schema = 'public' AND
        tc.constraint_type = 'FOREIGN KEY'
) AS column_definitions
GROUP BY
    table_name, foreign_key_column, foreign_table, referenced_column;


            """


def get_sql_for_all_migrations():
    # execute raw sql to get the sql for all migrations
    sql_commands = []
    with connection.cursor() as cursor:
        cursor.execute(statement)
        for row in cursor.fetchall():
            sql_commands.append(row[0])
    print(sql_commands)
    return sql_commands


# Create your views here.


@require_http_methods(["GET"])
def list_models(request: HttpRequest):
    url = settings.COPILOT_ENDPOINT + "models"
    response = requests.get(url)
    models = response.json()
    return JsonResponse(models)


def determine_action(msg: str) -> str:

    # call the  model to determine the action
    query = f"""
            SQL statements used to create the tables in the database: {get_sql_for_all_migrations()}
            Based on the message: {msg} generate the SQL statement that satisfies the request. If no sql statement can be generated, return 'none' else only return the SQL statement
            Only generate the SQL statement for the request without any explanation
            The SQL statement should only read from the database and not write to the database
            In case the query is to modify the database, return 'none'
            """
    action = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama3-70b-8192",
    )
    print(action.choices[0].message.content)
    return action.choices[0].message.content


def execute_action(sql: str):
    if sql.strip().lower().startswith("select"):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        # Convert the rows to dictionaries
        rows_as_dict = [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows
        ]

        # Convert the dictionaries to JSON
        json_data = json.dumps(rows_as_dict)
        return json_data
    return "none"


# @require_http_methods(["POST"])
def chat(request: HttpRequest):
    action = determine_action("Which was the latest sale?")
    print(action)
    res = ""
    if action == "none":
        pass
    else:
        res = execute_action(action)

    with connection.cursor() as cursor:
        cursor.execute(action)
        for row in cursor.fetchall():
            res += row[0]
    return JsonResponse({"action": action, "response": res, "sql": action})


def get_latest_sale():
    latest_sale = Sale.objects.latest("date_added")
    if latest_sale:
        return latest_sale.to_json()
