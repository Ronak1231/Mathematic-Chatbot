
# Math Chatbot 🤖

This is a simple Streamlit-based chatbot that allows users to perform various types of mathematical operations, including:

- **Arithmetic Operations**: Addition, subtraction, multiplication, division, etc.
- **Trigonometric Functions**: `sin(x)`, `cos(x)`, `tan(x)`, and more.
- **Unit Conversions**: Convert between units like meters to kilometers, miles to kilometers, Celsius to Fahrenheit, etc.
- **Plotting Functions**: Plot mathematical functions such as `sin(x)`, `cos(x)`, and other expressions.
- **Variable Assignment**: Users can define variables (e.g., `a = 5`) and use them in calculations.
- **Error Handling**: The chatbot provides feedback if there are any errors or invalid inputs.
- **History Tracking**: The chatbot keeps track of past calculations and displays them.

## Features

- **Arithmetic Expressions**: Enter mathematical expressions (e.g., `2 + 3`, `sin(x)`) and get the result.
- **Unit Conversion**: Convert units such as meters to kilometers, miles per hour to meters per second, etc.
- **Function Plotting**: Plot mathematical functions like `sin(x)` or `x**2` using SymPy and Matplotlib.
- **Variable Assignment**: Assign values to variables (e.g., `a = 5`) and use them in expressions.

## Installation

1. Clone the repository or download the Python file.
2. Install required dependencies:
   ```bash
   pip install streamlit numpy sympy matplotlib
   ```

## Running the Application

To run the chatbot application, use the following command:

```bash
streamlit run app.py
```

This will launch the Streamlit app in your default web browser, where you can interact with the chatbot.
