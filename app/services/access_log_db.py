"""Access log table."""
from sqlalchemy import Table, Column, Integer, String, create_engine, MetaData, select, func, and_
from datetime import datetime, timedelta

from app.config import ACCESS_LOG_DATABASE_URI

# Create a connection to the database
engine = create_engine(ACCESS_LOG_DATABASE_URI)

# Define database metadata
metadata = MetaData()

# Define the table dynamically
access_log_table = Table('access_log', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('agent', String(255)),
    Column('bytes_sent', Integer),
    Column('child_pid', Integer),
    Column('cookie', String(255)),
    Column('machine_id', String(25)),
    Column('request_file', String(255)),
    Column('referer', String(255)),
    Column('remote_host', String(50)),
    Column('remote_logname', String(50)),
    Column('remote_user', String(50)),
    Column('request_duration', Integer),
    Column('request_line', String(255)),
    Column('request_method', String(10)),
    Column('request_protocol', String(10)),
    Column('request_time', String(28)),
    Column('request_uri', String(255)),
    Column('request_args', String(255)),
    Column('server_port', Integer),
    Column('ssl_cipher', String(25)),
    Column('ssl_keysize', Integer),
    Column('ssl_maxkeysize', Integer),
    Column('status', Integer),
    Column('time_stamp', Integer),
    Column('virtual_host', String(255)),
    Column('date', String(255))
)


def query(selects=None, columns=None, filters=None, group_by=None, order_by=None, limit=None):
    """Execute a query on the access_log table."""
    # Create a base query
    if selects:
        query = select(selects)
    else:
        query = select(access_log_table)

    # Apply selected columns
    if columns:
        query = query.with_only_columns([access_log_table.columns[column] for column in columns])

    # Apply filters
    if filters is not None:
        query = query.where(filters)

    # Apply group by
    if group_by is not None:
        query = query.group_by(group_by)

    # Apply order by
    if order_by is not None:
        query = query.order_by(order_by)

    # Apply limit
    if limit is not None:
        query = query.limit(limit)

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()


def last_access_log_query(limit=10, ip_filter=None, user_login=False, additonal_columns=None):
    #parametros query
    selects = None
    
    columns = ['id', 'remote_host', 'date']

    if additonal_columns:
        for column in additonal_columns:
            columns.append(column)
    
    if ip_filter:
        filter = access_log_table.columns.remote_host != f'{ip_filter}'
    elif user_login is True:
        filter1 = access_log_table.columns.request_method == 'POST'
        filter2 = access_log_table.columns.request_uri == '/login/'
        filter = and_(filter1, filter2)
    else:
        filter = None
    
    order = access_log_table.columns.id.desc()


    resultados = query(selects=selects, columns=columns, filters=filter, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list


def most_accesses_by_ip_query(limit=10):
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    #parametros query
    selects = [access_log_table.c.remote_host,func.count().label('count'),func.max(access_log_table.c.date).label('last_access')]
    columns = None
    filters = access_log_table.c.date >= time_threshold
    group = access_log_table.c.remote_host
    order = func.count().desc()
    
    resultados = query(selects=selects, columns=columns, filters=filters, group_by=group, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list
