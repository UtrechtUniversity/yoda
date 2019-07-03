import itertools


__all__ = [
    "row_iterator",
    "paged_iterator",
    "AS_DICT",
    "AS_LIST",
]


MAX_SQL_ROWS = 256
AUTO_CLOSE_QUERIES = True
Report_Exit_To_Log = False

class row_return_type (object):
    def __init__(self): raise NotImplementedError

class AS_DICT (row_return_type): pass
class AS_LIST (row_return_type): pass

class bad_column_spec (RuntimeError): pass
class bad_returntype_spec (RuntimeError): pass


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::              generator-style query iterator              :::::
# :::::   --> yields one row  from query results per iteration   :::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def row_iterator(  columns,     # comma-separated string, or list, of columns
                   conditions,  # genquery condition eg. "COLL_NAME not like '%/trash/%'"
                   row_return,  # AS_DICT or AS_LIST to specify rows as Python 'list's or 'dict's
                   callback     # fed in directly from rule call argument
                ):

    import irods_types

    if not issubclass(row_return, row_return_type):
        raise bad_returntype_spec( "row_return parameter should be AS_DICT or AS_LIST" )

    if not isinstance(columns, (list, tuple)):
        if isinstance(columns, str):
            columns = list(map(lambda obj: obj.strip(), columns.split(",")))
        else:
            raise bad_column_spec ( "Column argument '{!r}' should be column names " \
                                    "as list or comma separated string".format(columns))

    if len(columns) < 1:
        raise bad_column_spec( "Must select at least one column for the query" )

    column_indices = list(map(reversed,enumerate(columns)))
    column_lookup = dict(column_indices)

    ret_val = callback.msiMakeGenQuery(",".join(columns) , conditions , irods_types.GenQueryInp())
    genQueryInp = ret_val['arguments'][2]

    ret_val = callback.msiExecGenQuery(genQueryInp , irods_types.GenQueryOut())
    genQueryOut = ret_val['arguments'][1]
    continue_index_old = 1

    ret_val = callback.msiGetContInxFromGenQueryOut( genQueryOut, 0 )
    continue_index = ret_val['arguments'][1]

    exit_type = ''

    try:

        while continue_index_old > 0:

            for j in range(genQueryOut.rowCnt):

                row_as_list = [ genQueryOut.sqlResult[i].row(j) for i in range(len(column_indices)) ]

                if row_return is AS_DICT:
                    yield { k : row_as_list[v] for k,v in column_lookup.items() }
                elif row_return is AS_LIST:
                    yield row_as_list

            continue_index_old = continue_index

            ret_val = None  #-- in case of exception from msiGetMoreRows call
            ret_val = callback.msiGetMoreRows(genQueryInp , genQueryOut, 0)

            genQueryOut = ret_val['arguments'][1]
            continue_index = ret_val['arguments'][2]

    except GeneratorExit:
        exit_type = 'ITERATION_STOPPED_BY_CALLER'
    except Exception as e:
        if ret_val is None:
            exit_type = 'GET_ROWS_ERROR'
        else:
            exit_type = 'UNKNOWN_ERROR'
        continue_index = 0 # prevent iterating through rest of results in "finally" clause
        raise                  # --> rethrow (run the finally clause, but then propagates exception)
    else:
        exit_type = '(Normal)'
    finally:
        if Report_Exit_To_Log:
            callback.writeLine("serverLog","Python GenQuery exit type - {}".format(exit_type))

        #callback.msiCloseGenQuery( genQueryInp, genQueryOut ) # prb not a good strategy from Python

        if AUTO_CLOSE_QUERIES:
            while continue_index > 0:
                continue_index_old = continue_index
                ret_val = callback.msiGetMoreRows(genQueryInp , genQueryOut, 0) 
                genQueryOut = ret_val['arguments'][1]
                continue_index = ret_val['arguments'][2]


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::           Page-at-a-time query iterator                     ::::
# ::::: --> Yields one page of 0<N<=MAX_SQL_ROWS results as a list  ::::
# :::::     of rows. As with the row_iterator, each row is either a ::::
#::::::     list or dict object (dictated by the row_return param)  ::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class paged_iterator (object):

    def __init__(self, columns, conditions, row_return, callback,
                 N_rows_per_page = MAX_SQL_ROWS):

        self.callback = callback
        self.set_rows_per_page ( N_rows_per_page , hard_limit_at_default = True )

        self.generator =  row_iterator (columns, conditions, row_return, callback )

    def __iter__(self): return self
    def __next__(self): return self.next()

    def set_rows_per_page (self, rpp, hard_limit_at_default = False):

        self.rows_per_page = max (1, int(rpp))

        if hard_limit_at_default:
            self.rows_per_page = min( self.rows_per_page,  MAX_SQL_ROWS )

        return self

    def next_arbitrary_size(self):

        this_page = list(itertools.islice(self.generator, self.rows_per_page))
        if 0 == len(this_page) : raise StopIteration
        return this_page

    def next(self):

        if self.rows_per_page > MAX_SQL_ROWS:

            return self.next_arbitrary_size()

        else:

            results = list( range(self.rows_per_page) )
            j = 0

            try:
                while j < len(results):
                    results[j] = next(self.generator)
                    j += 1
            except StopIteration:
                if j == 0: raise
            except Exception as e:
                self.callback.writeLine('serverLog',
                  '*** UNEXPECTED Exception in genquery.py paged iterate [next()]')
                self.callback.writeLine('serverLog','***   {!r}'.format(e))
                raise

            # -- truncate list size to fit the generated results
            del results[j:]

            return results

def logPrinter(callback, stream):
  return lambda logMsg : callback.writeLine( stream, logMsg )

#  ###############################################################################
#  Helper routine to set up or tear down (N*1000) AVU's on the logical collection
#    (with N between '0' and '9' inclusive)
#  Note -- 'imeta rum' can be used to clear the unused AVU's if necessary
#  ###############################################################################

def set_or_clear_gnx_test_meta_on_coll(collnpath , operation, N, callback,
                                       partial_pages = True):
    import irods_types
    if partial_pages:
        lower_bound = 0
    else:
        lower_bound = 1000 - 768
    thousands = 0
    meta_string = "kvp_page={}%" .format(thousands) + \
                  "%".join("{:04d}={}".format(i,-(i%10+1)) for i in range(lower_bound,1000))

    for thousands in range(int(N)):
        kvp = callback.msiString2KeyValPair(meta_string, irods_types.KeyValPair())['arguments'][1]
        if operation.upper() in ('ASSOC','SET','+'):
            retval = callback.msiAssociateKeyValuePairsToObj( kvp, collnpath,  "-C")
        elif operation.upper() in ('CLEAR', 'CLR', '-'):
            retval = callback.msiRemoveKeyValuePairsFromObj( kvp, collnpath,  "-C")
        meta_string = meta_string.replace(
                       "%{}".format(thousands),"%{}".format(thousands+1)).replace(
                       "={}".format(thousands),"={}".format(thousands+1))

#  ################################################################################
#  Test function for evaluating the auto close feature (AUTO_CLOSE_QUERIES -> True)
#     (test cases remain to be written as this flag is an experimental feature)
#  ################################################################################

def test_generator_exit_cases_Via_Rule_Framework (rule_args, callback, rei):

    test_generator_exit_cases_Via_DirectCall (*rule_args, callback_=callback, rei_=rei)

def test_generator_exit_cases_Via_DirectCall (*rule_args_ , **kw):

    callback = kw.get('callback_')
    rei = kw.get('rei_')

    coll_name = rule_args_[0]

    rowcount_and_mode =  rule_args_[1]
    test_params = ( rule_args_[1] ).lower().split(",")

    test_param_defaults = ["ROW",     "3",   "1",            "_"*4 ]
                          # itr_type, nQuery, nRepsPerQuery, likePattern

    if len(test_params)<4: test_params += test_param_defaults[ len(rmi)-4: ] # - extend with defaults

    iterType      =  test_params[0]
    nQueries      = int(test_params[1])
    nRepsPerQuery = int(test_params[2])
    likePattern   = test_params[3]

    if rule_args_[2:] and rule_args_[2] and (callback is not None):
        logger = logPrinter(callback, rule_args_[2])
    else:
        logger = lambda logMsg: None

    columns    = [ "META_COLL_ATTR_NAME", "META_COLL_ATTR_VALUE" ]
    conditions = "COLL_NAME = '{0}' ".format( coll_name )

    if test_params[3] != "":
        conditions += " and META_COLL_ATTR_NAME like '{}'".format(test_params[3])

    Iterator = (row_iterator if 'row' in iterType else paged_iterator)

    for j in range(nQueries):
        nObj = 0
        for obj in Iterator ( columns, conditions, AS_LIST, callback ):
            nObj += 1
            if nObj > nRepsPerQuery: break

#
#  Test rule below takes (like_path_rhs , requested_rowcount) as arguments via "rule_args" param
#
#    like_path_rhs :         {collection}/{dataname_sql_pattern} eg: '/myZone/home/alice/%'
#    requested_rowcount :    '<integer>' (for #rows-per-page) or '' (use generator)
#    detail logging stream : one of [ 'serverLog', 'stdout', 'stderr', '' ]
#

def test_python_RE_genquery_iterators( rule_args , callback, rei ):

    cond_like_RHS = rule_args[0]
    coll_name = "/".join(cond_like_RHS.split('/')[:-1])
    data_obj_name_pattern = cond_like_RHS.split('/')[-1]

    requested_rowcount = str( rule_args[1] )

    if rule_args[2:] and rule_args[2]:
        logger = logPrinter(callback, rule_args[2])
    else:
        logger = lambda logMsg: None

    conditions = "COLL_NAME = '{0}' AND DATA_NAME like '{1}'".format(
                  coll_name , data_obj_name_pattern )
    nr = 0
    n = 0

    last_page = None

    lists_generated  = 0
    lists_remainder = 0

    if len(requested_rowcount) > 0:

        rows_per_page = int(requested_rowcount)

        logger( "#\n#\n__query: (%d) rows at a time__"%(rows_per_page,) )
        for page in paged_iterator("DATA_NAME,DATA_SIZE" , conditions, AS_DICT, callback,
                                                         N_rows_per_page = rows_per_page ):
            i = 0
            logger("__new_page_from_query__")
            for row in page:

                logger( ("n={0},i={1} ; name = {2} ; size = {3}"
                        ).format(n, i, row['DATA_NAME'], row['DATA_SIZE'] ))
                n += 1
                i += 1
                nr += 1

            lists_generated += 1
            last_page = page

    else:

        logger( "__gen_mode_return_all_rows_from_query__" )

        for row in row_iterator( "DATA_NAME,DATA_SIZE" , conditions, AS_DICT, callback ):

            logger( ("n = {0} ; name = {1} ; size = {2}"
                          ).format( n, row['DATA_NAME'], row['DATA_SIZE'] ))
            n += 1
            nr += 1

    if lists_generated > 0:
        lists_remainder = len( last_page )

    rule_args[0] = str( nr ) # -> fetched rows total
    rule_args[1] = str( lists_generated )
    rule_args[2] = str( lists_remainder )

