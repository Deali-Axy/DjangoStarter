from django_starter import constants


def table_name_wrapper(table_name: str) -> str:
    """
    包装 DjangoStarter 数据表名

    :param table_name:
    :return:
    """
    return f'{constants.db_table_prefix}_{table_name}'
