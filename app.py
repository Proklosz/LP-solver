from ortools.linear_solver import pywraplp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def SolveAndPrint(solver, variable_list, constraint_list, is_precise):
    """Solve the problem and print the solution."""
    result_status = solver.Solve()

    # The problem has an optimal solution.
    assert result_status == pywraplp.Solver.OPTIMAL

    # The solution looks legit (when using solvers others than
    # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    if is_precise:
        assert solver.VerifySolution(1e-7, True)

    print("Problem solved in %f milliseconds" % solver.wall_time())

    # The objective value of the solution.
    print("Optimal objective value = %f" % solver.Objective().Value())

    # The value of each variable in the solution.
    result =''
    for variable in variable_list:
        print("%s = %f" % (variable.name(), variable.solution_value()))
        if(result == ''):
            result = result + str("%s = %d " % (variable.name(), variable.solution_value()))
        else:
            result = result + "  ||  " + str("%s = %d " % (variable.name(), variable.solution_value()))

    print("Advanced usage:")
    print("----Problem solved in %d iterations" % solver.iterations())
    
    
    # result = variable[0], variable[1], variable[2]
    return result

def RunLinearExampleNaturalLanguageAPI(data):
    """Example of simple linear program with natural language API."""
    solver = pywraplp.Solver.CreateSolver("CBC_MIXED_INTEGER_PROGRAMMING")

    if not solver:
        return None

    variable_values = data['variable_values']
    senSes = data["senSes"]
    RHS = data['RHS']
    ProblemSense = data['ProblemSense']

    infinity = solver.infinity()
    # x1, x2, and x3 are now integer variables.
    x1 = solver.IntVar(0, infinity, "x1")
    x2 = solver.IntVar(0, infinity, "x2")
    x3 = solver.IntVar(0, infinity, "x3")

    if(ProblemSense == "MAX"):
        solver.Maximize(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3)
    else:
        solver.Minimize(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3)
    
    if(str(senSes[0]) == "G"):
        c0 = solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 >= RHS[0])
    elif(str(senSes[0]) == "L"):
        c0 = solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 <= RHS[0]) 

    if(str(senSes[1]) == "G"):
        c1 = solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 >= RHS[1])
    elif(str(senSes[1]) == "L"):
        c1 = solver.Add(variable_values[0] * x1 + variable_values[1] * x2 + variable_values[2] * x3 <= RHS[1])    
        
   

    result = SolveAndPrint(solver, [x1, x2, x3], [c0, c1], True)
    return result

@app.route('/')
def index():
    return "Welcome to the API Tester!"

@app.route('/calculate', methods=['POST'])
def calculate_sum():
    try:
        data = request.get_json()
        result = RunLinearExampleNaturalLanguageAPI(data)
        if result is not None:
            print(str(result))
            return jsonify(result)
            
        else:
            return jsonify({'error': 'Solver creation failed.'}), 500
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
