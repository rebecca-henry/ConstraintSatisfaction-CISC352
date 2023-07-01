# =============================
# Student Names: Rebecca Henry
# Group ID: 29
# Date: 02/16/22
# =============================
# CISC 352 - W22
# heuristics.py
# desc: degree heuristic and minimum remaining value heuristic implementation
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    unVars = csp.get_all_unasgn_vars()
    nextVar = unVars[0]
    nextVarCount = 0
    # keep track of the variable with maximum amount of constraints
    # with unassigned vars and compare all other vars to it, adjusting as needed
    for curVar in unVars:
        curCount = 0
        for con in csp.get_cons_with_var(curVar):
            if con.get_n_unasgn() > 0:
                curCount += 1
        if curCount > nextVarCount:
            nextVar = curVar
            nextVarCount = curCount
    return nextVar

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    unVars = csp.get_all_unasgn_vars()
    nextVar = unVars[0]
    smallDomSize = nextVar.cur_domain_size()
    for curVar in unVars:   #compare each unassigned variable to the assigned nextVar
        if curVar.cur_domain_size() < smallDomSize: #is it smaller than the smallest
            nextVar = curVar #reassign nextVar to the smallest variable
            smallDomSize = curVar.cur_domain_size()
    return nextVar
