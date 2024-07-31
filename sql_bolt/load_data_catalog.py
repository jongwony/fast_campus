import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from google.cloud import bigquery

from dotenv import load_dotenv

load_dotenv()


def get_values(spreadsheet_id, range_name):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id, and range_name
    results = get_values(
        "1S5kQhnRyXKPWqqN9db9_GE_qtCT8oFqFGLG7tsUj5Sg", "chinook")
    df = pd.DataFrame(results['values'][1:], columns=results['values'][0])

    # Construct a BigQuery client object.
    client = bigquery.Client()
    project = 'sigma-kayak-430300-a2'
    dataset = 'chinook'

    for grouped, chunk in df.groupby(['테이블명', '테이블설명']):
        table_name, table_description = grouped
        column_map = chunk.set_index('컬럼명')['설명'].to_dict()
        print(table_name)
        table_id = f"{project}.{dataset}.{table_name}"

        table = client.get_table(table_id)  # Make an API request.
        table.description = table_description

        new_schema = [
            bigquery.SchemaField(
                schema.name,
                schema.field_type,
                mode=schema.mode,
                description=column_map[schema.name],
            )
            for schema in table.schema
        ]
        table.schema = new_schema
        # Make an API request.
        table = client.update_table(table, ["schema", "description"])
