from db.querybuilder.querybuilder import QueryBuilder
from db.querybuilder.abstractquerybuilder import SortOrder, Operation, MatchMode
from db.querybuilder.expressions import Parentheses, SimpleExpression


def testEqExpression():
    testQuery = 'select field from table_name'
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'

    builder = QueryBuilder(testQuery)
    builder.eq(eqFieldName, eqValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [eqValue]
    assert query == f'{testQuery} where {eqFieldName} = ?'

def testParenthesesExpression():
    testQuery = 'select field from table_name'
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'

    builder = QueryBuilder(testQuery)
    exExp = SimpleExpression(eqFieldName, eqValue, Operation.EQ)
    builder.parentheses(exExp)
    
    query = builder.getQuery()

    assert query == f'{testQuery} where ({eqFieldName} = ?)'

def testSortByWithOneSortingField():
    testQuery = 'select field from table_name'
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'
    sortField = 'sort_field_name'
    sortOrder = SortOrder.ASC

    builder = QueryBuilder(testQuery)
    builder.eq(eqFieldName, eqValue)
    builder.addSorting(sortField, sortOrder)
    
    query = builder.getQuery()

    assert query == f'{testQuery} where {eqFieldName} = ? order by {sortField} {sortOrder.value}'

def testSortOrderWithMultipleSortingField():
    testQuery = 'select field from table_name'
    sortFieldOne = 'sort_field_name_one'
    sortOrderOne = SortOrder.ASC
    sortFieldTwo = 'sort_field_name_two'
    sortOrderTwo = SortOrder.DESC

    builder = QueryBuilder(testQuery)
    builder.addSorting(sortFieldOne, sortOrderOne)
    builder.addSorting(sortFieldTwo, sortOrderTwo)
    
    query = builder.getQuery()

    assert query == f'{testQuery} order by {sortFieldOne} {sortOrderOne.value}, {sortFieldTwo} {sortOrderTwo.value}'

def testPaging():
    testQuery = 'select field from table_name'
    startIndex = 0
    count = 10
    testArguments = [startIndex, count - 1]

    builder = QueryBuilder(testQuery)
    builder.addPaging(startIndex, count)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} limit ?, ?'

def testBuilderConstructorWithParameters():
    testQuery = 'select field from table(func_name(?,?,?))'
    testArguments = [1, 2, 3]

    builder = QueryBuilder(testQuery, testArguments)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == testQuery

def testBuilderOperationWithExitingParameters():
    testQuery = 'select field from table(func_name(?,?,?))'
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'
    exitingArgs = [1, 2, 3]
    testArguments = []
    testArguments.extend(exitingArgs)
    testArguments.append(eqValue)

    builder = QueryBuilder(testQuery, exitingArgs)
    builder.eq(eqFieldName, eqValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} where {eqFieldName} = ?'

def testNeForValue():
    testQuery = 'select field from table_name'
    neValue = 'ne_value'
    neFieldName = 'ne_field_name'

    builder = QueryBuilder(testQuery)
    builder.neForValue(neFieldName, neValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [neValue]
    assert query == f'{testQuery} where {neFieldName} != ?'

# TODO - одинаковый результат с neForValue
def testNeForString():
    testQuery = 'select field from table_name'
    neValue = 'ne_value'
    neFieldName = 'ne_field_name'

    builder = QueryBuilder(testQuery)
    builder.neForString(neFieldName, neValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [neValue]
    assert query == f'{testQuery} where {neFieldName} != ?'

def testLike():
    testQuery = 'select field from table_name'
    likeValue = 'ne_value'
    likeFieldName = 'ne_field_name'

    builder = QueryBuilder(testQuery)
    builder.like(likeFieldName, likeValue, MatchMode.EXACT)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [likeValue]
    assert query == f'{testQuery} where {likeFieldName} like ?'

def testIlike():
    testQuery = 'select field from table_name'
    iLikeValue = 'ne_value'
    iLikeFieldName = 'ne_field_name'

    builder = QueryBuilder(testQuery)
    builder.iLike(iLikeFieldName, iLikeValue, MatchMode.EXACT)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == [iLikeValue]
    assert query == f'{testQuery} where upper({iLikeFieldName}) like ?'

def testBeetween():
    testQuery = 'select field from table_name'
    fromValue = 'from_value'
    toValue = 'to_value'
    beetweenFieldName = 'ne_field_name'
    testArguments = [fromValue, toValue]

    builder = QueryBuilder(testQuery)
    builder.between(beetweenFieldName, fromValue, toValue)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} where {beetweenFieldName} >= ? and {beetweenFieldName} <= ?'

def testIsNull():
    testQuery = 'select field from table_name'
    nullFieldName = 'null_field_name'

    builder = QueryBuilder(testQuery)
    builder.isNull(nullFieldName)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == []
    assert query == f'{testQuery} where {nullFieldName} is null'

def testIsNotNull():
    testQuery = 'select field from table_name'
    notNullFieldName = 'null_field_name'

    builder = QueryBuilder(testQuery)
    builder.isNotNull(notNullFieldName)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == []
    assert query == f'{testQuery} where {notNullFieldName} is not null'

def testInExp():
    testQuery = 'select field from table_name'
    inFieldName = 'in_field_name'
    testArguments = ['arg1', 'arg2', 'arg3']

    builder = QueryBuilder(testQuery)
    builder.inExp(inFieldName, testArguments)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} where {inFieldName} in (?, ?, ?)'

def testNotExp():
    testQuery = 'select field from table_name'
    eqValue = 'eq_value'
    eqFieldName = 'eq_field_name'
    testArguments = [eqValue]

    builder = QueryBuilder(testQuery)
    eqExp = SimpleExpression(eqFieldName, eqValue, Operation.EQ)
    parantheses = Parentheses(eqExp)
    builder.notExp(parantheses)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} where not ({eqFieldName} = ?)'

def testSimpleOperationForValueMethod():
    testQuery = 'select field from table_name'
    operValue = 'eq_value'
    operFieldName = 'eq_field_name'
    operation = Operation.NE
    testArguments = [operValue]

    builder = QueryBuilder(testQuery)
    builder.simpleOperationForValue(operFieldName, operValue, operation)
    
    query = builder.getQuery()
    arguments = builder.getArguments()

    assert arguments == testArguments
    assert query == f'{testQuery} where {operFieldName} != ?'