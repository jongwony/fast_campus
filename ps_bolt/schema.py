def test_create_table_query():
    return """
    CREATE TABLE `chinook.mytable` (
        `id` INT64 OPTIONS(description="The primary key"),
        `name` STRING OPTIONS(description="The name of the user"),
        `email` STRING OPTIONS(description="The email of the user"),
        `created_at` STRING OPTIONS(description="The time the user was created")
    ) OPTIONS(description="A table to store user information");
    """


def generate_create_table_query(table_schema, table_name, columns, table_description=None):
    query = f"CREATE TABLE `{table_schema}.{table_name}` (\n"
    for column in columns:
        query += f' `{column["column_name"]}` `{column["data_type"]}` OPTIONS(description="{column["description"]}"),\n'
    query = query.rstrip(',\n')
    query += '\n)'
    if table_description:
        query += f' OPTIONS(description="{table_description}")'
    query += ";"
    return query


if __name__ == '__main__':
    create_table_str = generate_create_table_query(
        table_schema='chinook',
        table_name='mytable',
        columns=[
            {
                "column_name": "id",
                "data_type": "INT64",
                "description": "The primary key",
            },
            {
                "column_name": "name",
                "data_type": "STRING",
                "description": "The name of the user",
            },
            {
                "column_name": "email",
                "data_type": "STRING",
                "description": "The email of the user",
            },
            {
                "column_name": "created_at",
                "data_type": "STRING",
                "description": "The time the user was created",
            }
        ],
        table_description='A table to store user information',
    )
