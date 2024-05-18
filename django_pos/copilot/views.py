from datetime import datetime
import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
from dotenv import load_dotenv
import os
from django.db import connection
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def preprocess_data_for_presentation(data: str) -> str:
    """
    Prompt the AI model to convert the data into html format for presentation
    """
    query = f"""
            Convert the data into html format for presentation
            Data: {data}
            If the data can be converted into a table, return the table in html format. Use Bootstrap styling
            Only generate the html code without any explanation, for example the following response is not valid:
            'Here is the html code to for the best selling products in table format:\n\n```\n<table>\n<tr><th>Product Name</th><th>Total Sold</th></tr>\n<tr><td>Product 1</td><td>100</td></tr>\n<tr><td>Product 2</td><td>90</td></tr>\n</table>\n```'
            instead, the response should be:
            '<table><tr><th>Product Name</th><th>Total Sold</th></tr><tr><td>Product 1</td><td>100</td></tr><tr><td>Product 2</td><td>90</td></tr></table>'
            The tables should have table-responsive class to make them scrollable on small screens
            If the data cannot be converted into a table, return the data as a paragraph
            """
    html = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama3-70b-8192",
    )
    # log query and response
    logger.info(f"Query: {query} Response: {html.choices[0].message.content}")
    return html.choices[0].message.content


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

    return sql_commands


def determine_action(msg: str) -> str:

    # call the  model to determine the action
    query = f"""
            SQL statements used to create the tables in the database: {get_sql_for_all_migrations()}
            Based on the message: {msg} generate the SQL statement that satisfies the request. If no sql statement can be generated, return 'none' else only return the SQL statement

            Please include table names in the SQL statement within "", for example, SELECT * FROM "Products", and not  SELECT * FROM Products
            Be care when perfoming joins, for example the statement:
            SELECT "Product".name, SUM("SaleItems".quantity) as total_sold
            FROM "SaleItems"
            JOIN "Product" ON "SaleItems".product_id = "Product".id
            GROUP BY "Product".name
            ORDER BY total_sold DESC
            LIMIT 1;
            would result in an errore because the column product_id does not exist in the SaleItems table, 
            the correct statement should be:
            SELECT "Product".name, SUM("SaleItems".quantity) as total_sold
            FROM "SaleItems"
            JOIN "Product" ON "SaleItems".product = "Product".id
            GROUP BY "Product".name
            ORDER BY total_sold DESC
            LIMIT 1;

            Only generate the SQL statement for the request without any explanation, for example the following response is not valid:
            	'Here is the SQL statement to generate a list of all products in the database:\n\n```\nSELECT * FROM "Product"\n```'
            instead, the response should be:
            'SELECT * FROM "Product"'
            The SQL statement should only read from the database and not write to the database
            In case the query is to modify the database, return 'none'
            """
    action = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama3-70b-8192",
    )
    # log query and response
    logger.info(f"Query: {query} Response: {action.choices[0].message.content}")

    return action.choices[0].message.content


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime objects to string in ISO 8601 format
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


def execute_action(sql: str):
    if sql.strip().lower().startswith("select"):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            logger.info(f"SQL: {sql} Response: {rows}")

        # Convert the rows to dictionaries
        rows_as_dict = [
            dict(zip([column[0] for column in cursor.description], row)) for row in rows
        ]

        # Convert the dictionaries to JSON
        json_data = json.dumps(rows_as_dict, cls=DateTimeEncoder)
        return json_data
    return "none"


@require_http_methods(["POST"])
@login_required(login_url="/users/login/")
@csrf_exempt
def chat(request: HttpRequest):
    query = request.POST.get("query", "")
    action = determine_action(query)
    html = ""

    res = ""
    if action == "none":
        pass
    else:
        res = execute_action(action)
        if res != "none":
            html = preprocess_data_for_presentation(res)

    return JsonResponse(
        {"action": action, "response": res, "sql": action, "html": html}
    )
