from flask import Flask, request, jsonify

from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your app


@app.route("/")
def index():
    return "Welcome to the API Tester!"


@app.route("/calculate", methods=["POST"])
def calculate_sum():
    try:
        data = request.get_json()
        variable_values = data["variable_values"]
        senSes = data["senSes"]
        RHS = data["RHS"]
        ProblemSense = data["ProblemSense"]

        variable_number = len(variable_values)
        constrains_number = len(senSes)

        import cplex

        # CPLEX problem object
        problem = cplex.Cplex()

        # craete var names
        var_names = ["x_" + str(i) for i in range(variable_number)]

        for i in range(variable_number):
            # variables
            problem.variables.add(names=[var_names[i]])

            # coefficients
            problem.objective.set_linear(var_names[i], 1)

            # VarToInteger
            problem.variables.set_types(var_names[i], problem.variables.type.integer)

        # Constraints
        for i in range(constrains_number):
            problem.linear_constraints.add(
                lin_expr=[cplex.SparsePair(ind=var_names, val=variable_values)],
                senses=[senSes[i]],
                rhs=[RHS[i]],
            )

        # ProblemSense
        if ProblemSense == "MAX":
            problem.objective.set_sense(problem.objective.sense.maximize)
        elif ProblemSense == "MIN":
            problem.objective.set_sense(problem.objective.sense.minimize)

        # Solve the problem
        problem.solve()

        # debug.lp
        problem.write("debug.lp")

        # Get the solution status and values of variables
        # solution_status = problem.solution.get_status()
        x_value = problem.solution.get_values()
        # objective_value = problem.solution.get_objective_value()

        # You can also send this result as a JSON response
        return jsonify({"result": x_value})

    except ValueError:
        return jsonify({"error": "Invalid input. Please enter valid numbers."}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
