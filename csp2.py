from ortools.linear_solver import pywraplp
import random

subcreated = False

def SolveAndPrint_Sub(sub_solver, variable_list, constraint_list, is_precise):

    global subcreated

    result_status = sub_solver.Solve()

    if(result_status != pywraplp.Solver.OPTIMAL):
        for i in range(len(Dual)):
            if(Dual[i]<2):
                for e in range(len(Dual)):
                    Dual[e]=0
                Dual[i]=2
                SubProblem(data, Dual)


    if is_precise:
        assert sub_solver.VerifySolution(1e-11, True)

    
    # print("Sub-Problem solved in %f milliseconds" % sub_solver.wall_time())
    # print("Sub-Problem Optimal objective value = %f" % sub_solver.Objective().Value())

    result = []
    for variable in variable_list:
        result.append(variable.solution_value())
 
    # print("Sub-Problem solved in %d iterations" % sub_solver.iterations())
    
    return result

def SubProblem(data, Dual):
    global subcreated
    
    sub_solver = pywraplp.Solver.CreateSolver("CBC_MIXED_INTEGER_PROGRAMMING")

    if not sub_solver:
        return None
    
    variable_values = data[0]
    RHS = data[2]

    infinity = sub_solver.infinity()
    x1 = sub_solver.IntVar(Dual[0], infinity, "x1")
    x2 = sub_solver.IntVar(Dual[1], infinity, "x2")
    x3 = sub_solver.IntVar(Dual[2], infinity, "x3")

    # Set variable bounds to achieve a similar effect
    

    sub_solver.Maximize(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3)
    c1 = sub_solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 <= RHS[0])

    pattern = SolveAndPrint_Sub(sub_solver, [x1, x2, x3], [c1], True)
    
    pattern_lot.append(pattern)
    
        # pattern_lot.append(pattern)
    print(f"--------------Új minta :           {pattern}")
        # print(pattern_lot)
    
    subcreated = True
    return pattern

def SolveAndPrint_Master(master_solver, variable_list, constraint_list, is_precise, Dual, pattern):
    result_status = master_solver.Solve()
    

    if(result_status != pywraplp.Solver.OPTIMAL):
        for i in range(len(data[0])):
            if(pattern[i]<1):
                for e in range(len(Dual)):
                    Dual[e]=0
                Dual[i] = 2
                # pattern = SubProblem(data, Dual)
                pattern = SubProblem(data, Dual)
                MasterProblem(data, pattern)
          # Generate a new pattern if the master problem is infeasible
        # Update variable_values based on pattern here as needed

    if is_precise:
        assert master_solver.VerifySolution(1e-11, True)
    
    # print("Master-Problem solved in %f milliseconds" % master_solver.wall_time())
    # print("Master-Problem Optimal objective value = %f" % master_solver.Objective().Value())

    result = []
    for variable in variable_list:
        result.append(variable.solution_value())
    # print("Master-Problem solved in %d iterations" % master_solver.iterations())
    
    return result

def MasterProblem(data, pattern):
    master_solver = pywraplp.Solver.CreateSolver("CBC_MIXED_INTEGER_PROGRAMMING")
    if not master_solver:
        return None
    variable_values = [0, 0, 0]
    if(pattern):
        for i in range(len(data[0])):
            
            # if((data[0][i] * pattern[i]) > variable_values[i]):
            #     variable_values[i] = data[0][i] * pattern[i]
            pattern = [sum(values) for values in zip(*pattern_lot)]
            variable_values[i] = pattern[i]
                
            # variable_values.append(data[0][i]*pattern[i])
    
    
        
    
    RHSF = data[1]
    # Define or pass data here as needed

    infinity = master_solver.infinity()
    x1 = master_solver.IntVar(0, infinity, "x1")
    x2 = master_solver.IntVar(0, infinity, "x2")
    x3 = master_solver.IntVar(0, infinity, "x3")

    master_solver.Minimize(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3)
    c1 = master_solver.Add(variable_values[0] * x1 >= RHSF[0])
    c2 = master_solver.Add(variable_values[1] * x2 >= RHSF[1])
    c3 = master_solver.Add(variable_values[2] * x3 >= RHSF[2])

    def ExportLpModel(master_solver, MSTR):
        lp_model = master_solver.ExportModelAsLpFormat(False)
        with open(MSTR, 'w') as file:
            file.write(lp_model)

    ExportLpModel(master_solver, "MSTR.lp")

    # Define constraints and objective function here
    
    # pattern_lot.append(pattern)

    finalresult = SolveAndPrint_Master(master_solver, [x1, x2, x3], [c1, c2, c3], True, Dual, pattern)
    numUsedRods = sum(finalresult)
    # print(f"-------------------------------Master debug:{variable_values}")
    
    print(f"--------------Variable values :    {variable_values}")
    print(f"Megkezdett rudak :                 {numUsedRods}")
    print(f"Mennyiségek :                      {finalresult}")
    print(f"Minták :                           {pattern_lot}")
    return finalresult

if __name__ == '__main__':
    pattern_lot = []
    
    Dual = [0, 0, 0]
    data = [[4, 6, 7], [80, 50, 100], [15]] 
    pattern = SubProblem(data, Dual)
    result = []
    result.append(MasterProblem(data, pattern))
    
    print(result)
