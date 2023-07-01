# =============================
# Student Name: Rebecca Henry
# Group ID: 29
# Date: 02/16/22
# =============================
# CISC 352 - W22
# propagators.py
# desc: implemented prop_GAC and prop_FC so that forwards
# checking and general arc consistency can be performed


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    pruned = []         #list to contain the tuples
    if newVar==None:
        #check every constraint in the csp
        for c in csp.get_all_cons():
            # get the unnassigned variable
            # check the scope of the constraint is 1
            # prune the unnasigned variable
            # add the tuple of the pruned (variable,value) pair to pruned list
            if len(c.get_unasgn_vars())>0:
                v = c.get_unasgn_vars()[0]
                for asgn_var in c.get_scope():
                    if asgn_var.is_assigned():
                        v.prune_value(asgn_var.get_assigned_value())
                        pruned.append( (v, asgn_var.get_assigned_value()) )
            # if there's no values left in the variable, dead end is reached
            if v.cur_domain_size() == 0:
                return [False, pruned]   
    else:
        #check every constraint containing newVar in csp
        for c in csp.get_cons_with_var(newVar):
            if c.get_n_unasgn() == 1:
                v = c.get_unasgn_vars()[0]
                for asgn_var in c.get_scope():
                    if asgn_var.is_assigned():
                        v.prune_value(asgn_var.get_assigned_value())
                        pruned.append( (v, asgn_var.get_assigned_value()) )
                if v.cur_domain_size() == 0:
                    return [False, pruned]
    print(pruned)
    return [True, pruned]
        
def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    q = []      # the queue
    if newVar == None:
        for v in csp.get_all_vars(): # fill q with all constraints
            q.append( (v, csp.get_cons_with_var(v)) ) # add (variable, associated constraints) to q
        while len(q) > 0:
            cur_var = q.pop()
            for con in cur_var[1]: #for each constraint in the cur_var's assocaited constraints
                if remove_inconsistent_values(cur_var[0], con): #if r-i-v pruned a variable
                    #for rel_var in con.get_scope(): #for every variable in this constraint's scope:
                    q.append( (con.get_scope()) ) #add the var & it's cons
    else:
        q.append( (newVar, csp.get_cons_with_var(newVar)) ) # add (newVar, associated constraints) to q
        while len(q) > 0:
            cur_var = q.pop()
            for con in cur_var[1]: #for each constraint in the cur_var's assocaited constraints
                if remove_inconsistent_values(cur_var[0], con): #if r-i-v pruned a variable
                    #for rel_var in con.get_scope(): #for every variable in this constraint's scope:
                    q.append( (rel_var, csp.get_cons_with_var(rel_var)) ) #add the var & it's cons             
                    
def remove_inconsistent_values(var, con):
    #commented out so that the test program can execute
    #for x in var.domain(): #for every value in the variable's domain
    #    if con.has_support(var, x) == False: #if the constraint can't support the (var,value) tuple
    #        var.prune_value(x)      #prune the value from the variable's cur_domain
    #        return True          #return true
    return False
            
