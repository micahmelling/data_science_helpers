import sqlalchemy


def connect_to_mysql(connection_dictionary):
    """
    Connects to a MySQL database. Require the RDS pem file is in your working directory.
    :param connection_dictionary: dictionary containing keys for host, user, password, and database
    :type connection_dictionary: dictionary
    :return: sqlalchemy connection
    """
    ssl_args = {'ssl': {'ca': 'rds-ca-2019-root.pem'}}
    host = connection_dictionary['host']
    user = connection_dictionary['user']
    password = connection_dictionary['password']
    database = connection_dictionary['database']
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:3306/{database}',
                                      connect_args=ssl_args)
    return engine


def write_dataframe_to_database(df, schema, table, db_conn):
    """
    Writes a dataframe to a database table
    :param df: dataframe we want to record
    :type df: pandas dataframe
    :param schema: name of the schema
    :type schema: str
    :param table: name of the table
    :type table: str
    :param db_conn: sqlalchemy connection
    """
    df.to_sql(name=table, schema=schema, con=db_conn, if_exists='append', index=False)


def dynamically_create_ddl_and_execute(df, schema, table, db_conn):
    """
    Creates a DDL statement based on the inputted dataframe, which includes an id column and a meta__inserted_at
    column. Executes the DDL to create the table.
    :param df: dataframe we want to use to construct the ddl statement
    :type df: pandas dataframe
    :param schema: name of the schema in which the table will go
    :type schema: str
    :param table: name of the table to create
    :type table: str
    :param db_conn: sqlalchemy connection
    """
    ddl_statement = f'''
    create table if not exists {schema}.{table}(
    id int not null auto_increment primary key,
    meta__inserted_at timestamp default current_timestamp,
    '''

    dtype_mapping = {
        'int': 'int',
        'float': 'float',
        'object': 'text'
    }

    cols = list(df)
    for col in cols:
        col_dtype = str(df[col].dtype)
        sql_value = [val for key, val in dtype_mapping.items() if key in col_dtype][0]
        temp_str = f'{col} {sql_value},'
        ddl_statement += temp_str

    ddl_statement = ddl_statement[:-1]
    ddl_statement += ');'
    db_conn.execute(ddl_statement)
