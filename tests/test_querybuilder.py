from db.querybuilder.querybuilder import QueryBuilder


def testEqExpression():
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'

    builder = QueryBuilder("select field from table_name")
    builder.eq(eqFieldName, eqValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [eqValue]
    assert query == f'select field from table_name {eqFieldName} = ?'
