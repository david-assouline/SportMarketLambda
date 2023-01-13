import boto3

from dynamodb import create_ddb_instance
from shares import Shares

client = create_ddb_instance()
users_table = client.Table('Users')
print(users_table.table_status)

shares_obj = Shares(users_table)
shares_obj.buy_shares("1", "Montreal Canadiens", "500")
