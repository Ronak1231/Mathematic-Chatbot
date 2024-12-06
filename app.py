import streamlit as st
import re
import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt

# List of valid functions for easier detection of possible typos
valid_functions = ['sin', 'cos', 'tan']

# Dictionary to store variable assignments
variables = {}

# Function to evaluate arithmetic expressions with variables
def evaluate_expression(expression):
    try:
        # Replace variables in the expression with their values
        for var, value in variables.items():
            expression = expression.replace(var, str(value))
        
        # Handle complex numbers
        if 'j' in expression:
            result = eval(expression.replace('j', 'j'))
        # Handle functions like sin, cos, tan, log, sqrt, exp
        elif 'sin(' in expression or 'cos(' in expression or 'tan(' in expression:
            result = eval(f"np.{expression}")
        else:
            result = eval(expression)
        return result
    except NameError as e:
        return f"Error: Undefined variable used. Please assign the variable first. ({str(e)})"
    except Exception as e:
        return f"Error: {str(e)}"

# Unit conversion function
def convert_units(expression):
    try:
        if 'meters' in expression and 'to kilometers' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = value / 1000
            return f"{value} meters = {result} kilometers"
        elif 'miles' in expression and 'to kilometers' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = value * 1.60934
            return f"{value} miles = {result:.4f} kilometers"
        elif 'Celsius' in expression and 'to Fahrenheit' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = (value * 9/5) + 32
            return f"{value} Celsius = {result} Fahrenheit"
        elif 'inches' in expression and 'to meters' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = value * 0.0254
            return f"{value} inches = {result:.4f} meters"
        elif 'miles per hour' in expression and 'to meters per second' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = value * 1609.34 / 3600
            return f"{value} miles per hour = {result:.4f} meters per second"
        elif 'calories' in expression and 'to joules' in expression:
            value = float(re.findall(r'\d+\.?\d*', expression)[0])
            result = value * 4.184
            return f"{value} calories = {result} joules"
        else:
            return "Conversion not recognized"
    except Exception as e:
        return f"Error in unit conversion: {str(e)}"

# Function to plot a mathematical function
def plot_function(expression):
    x = sp.symbols('x')
    try:
        func = sp.sympify(expression)  # Convert the string to a symbolic expression
    except Exception as e:
        return f"Error: {str(e)}"
    
    # Generate a range for x values
    x_vals = np.linspace(-10, 10, 400)
    y_vals = np.array([float(func.evalf(subs={x: val})) for val in x_vals])

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=f'Function: {expression}')
    plt.title(f'Plot of {expression}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

# History feature to track calculations
def update_history(user_input, result):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(f"{user_input} = {result}")

# Function to display the calculation history
def display_history():
    if 'history' in st.session_state and st.session_state.history:
        st.subheader("Calculation History")
        for entry in st.session_state.history:
            st.write(entry)

# Function to handle invalid input for unknown functions
def handle_invalid_input(expression):
    for func in valid_functions:
        if func[:3] in expression:  # Check for common typos
            return f"Did you mean `{func}({expression[4:]})`?"
    return "Error: Invalid function or expression. Please check the syntax."

# Check if all variables used in an expression are defined
def check_variables(expression):
    for var in re.findall(r'\b[a-zA-Z_]\w*\b', expression):
        if var not in variables:
            return f"Error: Undefined variable '{var}' used. Please assign the variable first."
    return None

def main():
    # Set page config and UI
    st.set_page_config(page_title="Math Chatbot 🤖", page_icon="🤖", layout="wide")
    st.title("Math Chatbot 🤖")
    st.markdown("""Welcome to the Math Chatbot! You can perform arithmetic, complex calculations, unit conversions, and plot functions. Type your expression below (e.g., `2 + 3`, `sin(x)`) and press Enter.""")

    # User input
    user_input = st.text_input("You:", "")

    if user_input:
        user_input = user_input.strip()

        # Handle variable assignment (e.g., "e = 1 + 2")
        if '=' in user_input:
            var_name, expr = user_input.split('=', 1)
            var_name = var_name.strip()
            expr = expr.strip()

            # Check if the expression uses any undefined variables
            variable_check = check_variables(expr)
            if variable_check:
                st.markdown(f"**Error:** {variable_check}")
            else:
                # Evaluate and store the result in the variables dictionary
                result = evaluate_expression(expr)
                result_str = str(result)  # Convert result to string to check for error
                if "Error" in result_str:  # If there's an error, show it
                    st.markdown(f"**Error:** {result_str}")
                else:
                    variables[var_name] = result
                    st.markdown(f"**Assigned:** {var_name} = {result}")
                update_history(user_input, result)
        # If the user wants to plot a function
        elif user_input.startswith("plot"):
            expression = user_input[5:].strip()  # Remove 'plot' from the expression
            plot_function(expression)
        else:
            # Handle arithmetic, complex expressions, or unit conversions
            variable_check = check_variables(user_input)
            if variable_check:
                st.markdown(f"**Error:** {variable_check}")
            else:
                if re.match(r'^[\d\s\+\-\*\/\(\)j\.]+$', user_input):
                    result = evaluate_expression(user_input)
                    result_str = str(result)  # Convert result to string to check for error
                    st.markdown(f"**Result:** {result_str}")
                    update_history(user_input, result)
                elif 'to' in user_input:
                    conversion_result = convert_units(user_input)
                    st.markdown(f"**Conversion Result:** {conversion_result}")
                    update_history(user_input, conversion_result)
                else:
                    st.markdown(f"**Error:** {handle_invalid_input(user_input)}")

    # Display calculation history
    display_history()

if __name__ == "__main__":
    main()
