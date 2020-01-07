from functools import reduce

def combine(*dfs):
    # combines all dataframes
    # returns new spark dataframe
    return reduce(ps.sql.DataFrame.union, dfs)