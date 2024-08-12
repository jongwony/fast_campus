from langchain.chains.sql_database.prompt import SQL_PROMPTS

template = SQL_PROMPTS['googlesql']
template.get_prompts()[0].pretty_print()
