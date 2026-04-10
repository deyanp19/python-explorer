# Math Module Documentation

## Overview

The `math_examples.py` file demonstrates various functions from Python's built-in `math` module. This module provides access to mathematical constants and functions defined in the C standard library, offering high-precision calculations for scientific computing, data analysis, and engineering applications.

## Module Import

Before using any functions from the `math` module, you must import it:

```python
import math
```

## Mathematical Constants

### `math.e`
Base of the natural logarithm (e ≈ 2.71828...)

**Usage:**
```python
print(f"math.e = {math.e}")
# Output: math.e = 2.718281828459045
```

**Applications:**
- Exponential growth/decay calculations
- Natural logarithm calculations
- Compound interest formulas
- Probability distributions

### `math.pi`
Ratio of a circle's circumference to its diameter (π ≈ 3.14159...)

**Usage:**
```python
print(f"math.pi = {math.pi}")
# Output: math.pi = 3.141592653589793
```

**Applications:**
- Circle area and circumference calculations
- Trigonometric functions
- Geometrical calculations involving circles
- Wave and oscillation formulas

### `math.inf`
Positive infinity

**Usage:**
```python
print(f"math.inf = {math.inf}")
# Output: math.inf = inf
```

**Applications:**
- Initial values in optimization algorithms
- Infinite bounds in calculations
- Comparison operations

### `math.nan`
Not-a-Number (NaN) value

**Usage:**
```python
print(f"math.nan = {math.nan}")
# Output: math.nan = nan
```

**Applications:**
- Representing undefined mathematical results
- Error flagging in calculations
- Floating-point operations

## Rounding Functions

### `math.ceil(x)`
Return the ceiling of x, the smallest integer greater than or equal to x.

**Usage:**
```python
print(f"ceil(1.1) = {math.ceil(1.1)}")
# Output: ceil(1.1) = 2
print(f"ceil(-1.1) = {math.ceil(-1.1)}")
# Output: ceil(-1.1) = -1
print(f"ceil(3.7) = {math.ceil(3.7)}")
# Output: ceil(3.7) = 4
```

### `math.floor(x)`
Return the floor of x, the largest integer less than or equal to x.

**Usage:**
```python
print(f"floor(1.1) = {math.floor(1.1)}")
# Output: floor(1.1) = 1
print(f"floor(-1.1) = {math.floor(-1.1)}")
# Output: floor(-1.1) = -2
print(f"floor(3.7) = {math.floor(3.7)}")
# Output: floor(3.7) = 3
```

### `math.trunc(x)`
Return the Real part of x by truncating (removing) the fractional part.

**Usage:**
```python
print(f"trunc(3.7) = {math.trunc(3.7)}")
# Output: trunc(3.7) = 3
print(f"trunc(-3.7) = {math.trunc(-3.7)}")
# Output: trunc(-3.7) = -3
print(f"trunc(0.5) = {math.trunc(0.5)}")
# Output: trunc(0.5) = 0
```

### Built-in `round(x)`
Round x to the nearest integer. Uses "banker's rounding" (round half to even).

**Usage:**
```python
print(f"round(3.7) = {round(3.7)}")
# Output: round(3.7) = 4
print(f"round(2.5) = {round(2.5)}")
# Output: round(2.5) = 2  # Banker's rounding
print(f"round(3.5) = {round(3.5)}")
# Output: round(3.5) = 4
```

### `math.fabs(x)`
Return the absolute value of x as a float.

**Usage:**
```python
print(f"fabs(-5) = {math.fabs(-5)}")
# Output: fabs(-5) = 5.0
print(f"fabs(5.7) = {math.fabs(5.7)}")
# Output: fabs(5.7) = 5.7
```

## Modulo Operations

### `math.fmod(x, y)`
Return the IEEE remainder of x/y, similar to the % operator but with slightly different behavior for negative numbers and floating-point division.

**Usage:**
```python
print(f"fmod(15.5, 2) = {math.fmod(15.5, 2)}")
# Output: fmod(15.5, 2) = 1.5
print(f"fmod(17, 5) = {math.fmod(17, 5)}")
# Output: fmod(17, 5) = 2.0
```

**Difference from % operator:**
```python
print(f"15.5 % 2 = {15.5 % 2}")        # 1.5
print(f"{15.5} % {2} = {15.5 % 2}")    # 1.5
print(f"fmod(15.5, 2) = {math.fmod(15.5, 2)}")  # 1.5
```

## Trigonometric Functions

All trigonometric functions use **radians**, not degrees. Use `math.radians()` to convert.

### `math.sin(x)`
Return the sine of x radians.

**Usage:**
```python
print(f"sin(math.pi/2) = {math.sin(math.pi/2)}")
# Output: sin(math.pi/2) = 1.0
print(f"sin(0) = {math.sin(0)}")
# Output: sin(0) = 0.0
```

**Common values:**
- sin(0) = 0
- sin(π/6) = 0.5
- sin(π/4) ≈ 0.707 (1/√2)
- sin(π/3) ≈ 0.866 (√3/2)
- sin(π/2) = 1

### `math.cos(x)`
Return the cosine of x radians.

**Usage:**
```python
print(f"cos(0) = {math.cos(0)}")
# Output: cos(0) = 1.0
print(f"cos(math.pi) = {math.cos(math.pi)}")
# Output: cos(math.pi) = -1.0
```

**Common values:**
- cos(0) = 1
- cos(π/6) ≈ 0.866 (√3/2)
- cos(π/4) ≈ 0.707 (1/√2)
- cos(π/3) = 0.5
- cos(π/2) = 0
- cos(π) = -1

### `math.tan(x)`
Return the tangent of x radians.

**Usage:**
```python
print(f"tan(math.pi/4) = {math.tan(math.pi/4)}")
# Output: tan(math.pi/4) = 1.0
print(f"tan(0) = {math.tan(0)}")
# Output: tan(0) = 0.0
```

**Warning:** tan(π/2) will return a very large number or infinity, and tan(π/2) is mathematically undefined.

### `math.asin(x)`
Return the arc sine of x, in radians (inverse sine).

**Usage:**
```python
print(f"asin(0.5) = {math.asin(0.5)}")
# Output: asin(0.5) = 0.5235987755982989
print(f"asin(0) = {math.asin(0)}")
# Output: asin(0) = 0.0
```

**Domain:** -1 ≤ x ≤ 1

### `math.acos(x)`
Return the arc cosine of x, in radians (inverse cosine).

**Usage:**
```python
print(f"acos(0) = {math.acos(0)}")
# Output: acos(0) = 1.5707963267948966
print(f"acos(1) = {math.acos(1)}")
# Output: acos(1) = 0.0
```

**Domain:** -1 ≤ x ≤ 1
**Range:** 0 to π radians

### `math.atan(x)`
Return the arc tangent of x, in radians (inverse tangent).

**Usage:**
```python
print(f"atan(1) = {math.atan(1)}")
# Output: atan(1) = 0.7853981633974483
print(f"atan(0) = {math.atan(0)}")
# Output: atan(0) = 0.0
print(f"atan(float('inf')) = {math.atan(float('inf'))}")
# Output: atan(inf) = 1.5707963267948966
```

**Range:** -π/2 to π/2 radians

### `math.degrees(x)`
Convert angle x from radians to degrees.

**Usage:**
```python
print(f"degrees(math.pi/2) = {math.degrees(math.pi/2)}")
# Output: degrees(math.pi/2) = 90.0
print(f"degrees(math.pi) = {math.degrees(math.pi)}")
# Output: degrees(math.pi) = 180.0
```

**Common conversions:**
- degrees(0) = 0°
- degrees(π/6) = 30°
- degrees(π/4) = 45°
- degrees(π/3) = 60°
- degrees(π/2) = 90°

### `math.radians(x)`
Convert angle x from degrees to radians.

**Usage:**
```python
print(f"radians(90) = {math.radians(90)}")
# Output: radians(90) = 1.5707963267948966
print(f"radians(180) = {math.radians(180)}")
# Output: radians(180) = 3.141592653589793
```

**Common conversions:**
- radians(0°) = 0
- radians(30°) = π/6
- radians(45°) = π/4
- radians(60°) = π/3
- radians(90°) = π/2

## Exponential and Logarithmic Functions

### `math.pow(x, y)`
Return x raised to the power y (as a float).

**Usage:**
```python
print(f"pow(2, 3) = {math.pow(2, 3)}")
# Output: pow(2, 3) = 8.0
print(f"pow(10, 2) = {math.pow(10, 2)}")
# Output: pow(10, 2) = 100.0
print(f"pow(2, -1) = {math.pow(2, -1)}")
# Output: pow(2, -1) = 0.5
```

**Note:** Returns a float, unlike the `**` operator which can return an integer.

### `math.sqrt(x)`
Return the square root of x (must be non-negative).

**Usage:**
```python
print(f"sqrt(4) = {math.sqrt(4)}")
# Output: sqrt(4) = 2.0
print(f"sqrt(2) = {math.sqrt(2)}")
# Output: sqrt(2) = 1.4142135623730951
print(f"sqrt(9) = {math.sqrt(9)}")
# Output: sqrt(9) = 3.0
```

### `math.exp(x)`
Return e raised to the power x (e^x).

**Usage:**
```python
print(f"exp(1) = {math.exp(1)}")
# Output: exp(1) = 2.718281828459045
print(f"exp(0) = {math.exp(0)}")
# Output: exp(0) = 1.0
print(f"exp(-1) = {math.exp(-1)}")
# Output: exp(-1) = 0.36787944117144233
```

**Applications:**
- Exponential growth/decay
- Probability distributions (exponential, normal)
- Physics calculations
- Financial modeling

### `math.log(x[, base])`
Return the logarithm of x to the base specified (default: e).

**Usage:**
```python
print(f"log(100) = {math.log(100)}")
# Output: log(100) = 4.605170185988092
print(f"log(100, 10) = {math.log(100, 10)}")
# Output: log(100, 10) = 2.0
print(f"log(1) = {math.log(1)}")
# Output: log(1) = 0.0
```

### `math.log10(x)`
Return the base-10 logarithm of x.

**Usage:**
```python
print(f"log10(1000) = {math.log10(1000)}")
# Output: log10(1000) = 3.0
print(f"log10(100) = {math.log10(100)}")
# Output: log10(100) = 2.0
print(f"log10(10) = {math.log10(10)}")
# Output: log10(10) = 1.0
```

### `math.log2(x)`
Return the base-2 logarithm of x.

**Usage:**
```python
print(f"log2(8) = {math.log2(8)}")
# Output: log2(8) = 3.0
print(f"log2(16) = {math.log2(16)}")
# Output: log2(16) = 4.0
print(f"log2(32) = {math.log2(32)}")
# Output: log2(32) = 5.0
```

**Applications:**
- Bitwise operations (find bit length)
- Computer science calculations
- Information theory

## Geometric Functions

### `math.hypot(x, y)`
Return the Euclidean norm, equivalent to √(x² + y²), the length of a vector from origin to point (x, y).

**Usage:**
```python
print(f"hypot(3, 4) = {math.hypot(3, 4)}")
# Output: hypot(3, 4) = 5.0
print(f"hypot(5, 12) = {math.hypot(5, 12)}")
# Output: hypot(5, 12) = 13.0
```

**Note:** More numerically stable than manually calculating √(x² + y²), especially for very large or very small numbers.

## Special Values Handling

### `math.isinf(x)`
Check if x is a positive or negative infinity.

**Usage:**
```python
print(f"isinf(float('inf')) = {math.isinf(float('inf'))}")
# Output: inf = True
print(f"isinf(float('-inf')) = {math.isinf(float('-inf'))}")
# Output: True
print(f"isinf(5) = {math.isinf(5)}")
# Output: False
```

### `math.isnan(x)`
Check if x is a NaN (Not a Number).

**Usage:**
```python
print(f"isnan(float('nan')) = {math.isnan(float('nan'))}")
# Output: nan = True
print(f"isnan(math.inf) = {math.isnan(math.inf)}")
# Output: False
print(f"isnan(5) = {math.isnan(5)}")
# Output: False
```

### `math.isfinite(x)`
Check if x is finite (not infinity or NaN).

**Usage:**
```python
print(f"isfinite(5) = {math.isfinite(5)}")
# Output: finite = True
print(f"isfinite(float('inf')) = {math.isfinite(float('inf'))}")
# Output: False
print(f"isfinite(float('nan')) = {math.isfinite(float('nan'))}")
# Output: False
```

## Complete Example Output

Here's the complete example code:

```python
import math

# Basic Operations
print(f"ceil(1.1) = {math.ceil(1.1)}")          # 2
print(f"floor(1.1) = {math.floor(1.1)}")      # 1
print(f"fabs(-5) = {math.fabs(-5)}")          # 5.0
print(f"fmod(15.5, 2) = {math.fmod(15.5, 2)}")# 1.5
print(f"trunc(3.7) = {math.trunc(3.7)}")      # 3
print(f"round(3.7) = {round(3.7)}")            # 4

# Trigonometry
print(f"sin(math.pi/2) = {math.sin(math.pi/2)}")     # 1.0
print(f"cos(0) = {math.cos(0)}")                      # 1.0
print(f"tan(math.pi/4) = {math.tan(math.pi/4)}")      # 1.0
print(f"asin(0.5) = {math.asin(0.5)}")                # 0.5235987755982989
print(f"acos(0) = {math.acos(0)}")                    # 1.5707963267948966
print(f"atan(1) = {math.atan(1)}")                    # 0.7853981633974483
print(f"degrees(math.pi/2) = {math.degrees(math.pi/2)}")  # 90.0
print(f"radians(90) = {math.radians(90)}")            # 1.5707963267948966

# Other
print(f"pow(2, 3) = {math.pow(2, 3)}")               # 8.0
print(f"sqrt(4) = {math.sqrt(4)}")                   # 2.0
print(f"exp(1) = {math.exp(1)}")                     # 2.718281828459045
print(f"log(100) = {math.log(100)}")                 # 4.605170185988092
print(f"log10(1000) = {math.log10(1000)}")           # 3.0
print(f"log2(8) = {math.log2(8)}")                   # 3.0
print(f"hypot(3, 4) = {math.hypot(3, 4)}")           # 5.0
print(f"sin(0), cos(0), tan(0) = {math.sin(0)}, {math.cos(0)}, {math.tan(0)}")
print(f"math.e = {math.e}")                           # 2.71828...
print(f"math.pi = {math.pi}")                         # 3.14159...
print(f"math.inf = {math.inf}")                       # inf
print(f"math.nan = {math.nan}")                       # nan
print(f"isinf(float('inf')) = {math.isinf(float('inf'))}")            # True
print(f"isnan(float('nan')) = {math.isnan(float('nan'))}")            # True
print(f"isfinite(5) = {math.isfinite(5)}")                 # True
```

**Expected Output:**
```
ceil(1.1) = 2
floor(1.1) = 1
fabs(-5) = 5.0
fmod(15.5, 2) = 1.5
trunc(3.7) = 3
round(3.7) = 4
sin(math.pi/2) = 1.0
cos(0) = 1.0
tan(math.pi/4) = 1.0
asin(0.5) = 0.5235987755982989
acos(0) = 1.5707963267948966
atan(1) = 0.7853981633974483
degrees(math.pi/2) = 90.0
radians(90) = 1.5707963267948966
pow(2, 3) = 8.0
sqrt(4) = 2.0
exp(1) = 2.718281828459045
log(100) = 4.605170185988092
log10(1000) = 3.0
log2(8) = 3.0
hypot(3, 4) = 5.0
sin(0), cos(0), tan(0) = 0.0, 1.0, 0.0
math.e = 2.718281828459045
math.pi = 3.141592653589793
math.inf = inf
math.nan = nan
inf = True
nan = True
finite = True
```

## Common Use Cases

### 1. Geometry Calculations

```python
# Calculate circle area
radius = 5
area = math.pi * radius ** 2
print(f"Circle area: {area}")

# Calculate hypotenuse
a, b = 3, 4
c = math.hypot(a, b)
print(f"Hypotenuse: {c}")
```

### 2. Statistical Functions

```python
# Normal distribution components
mean = 0
std_dev = 1
x = 1.0
z = (x - mean) / std_dev
pdf = (1 / math.sqrt(2 * math.pi)) * math.exp(-z**2 / 2)
print(f"Normal PDF value: {pdf}")
```

### 3. Financial Calculations

```python
# Compound interest
principal = 1000
rate = 0.05
time = 10
amount = principal * math.exp(rate * time)
print(f"Compound interest: ${amount:.2f}")
```

### 4. Signal Processing

```python
# Convert degrees to radians for sine wave
time = [i * 0.1 for i in range(10)]
amplitude = 5
signal = [amplitude * math.sin(2 * math.pi * 0.5 * t) for t in time]
print(f"Sine wave samples: {signal}")
```

## Error Handling

### Common Errors and Solutions

**ValueError: math domain error**
```python
# Occurs when domain requirements aren't met
print(math.sqrt(-1))  # ValueError
print(math.acos(2))   # ValueError (domain: -1 to 1)
print(math.log(-1))   # ValueError (domain: > 0)

# Solution: Check domain before operating
x = -1
if x >= 0:
    print(math.sqrt(x))
else:
    print("Cannot take square root of negative number")
```

**OverflowError**
```python
# Exceptionally large values can cause overflow
print(math.exp(1000))  # May cause OverflowError
```

## Best Practices

1. **Always import the module first**
   ```python
   import math
   ```

2. **Use appropriate functions for precision needs**
   - `math.sqrt()` for square roots
   - `x ** 0.5` can work for square root too

3. **Remember trigonometric functions use radians**
   ```python
   math.sin(math.pi / 4)  # Correct
   math.sin(45)           # Wrong (45 degrees, not radians)
   ```

4. **Handle domain errors gracefully**
   ```python
   try:
       result = math.sqrt(negative_number)
   except ValueError as e:
       print(f"Cannot calculate: {e}")
   ```

5. **Use `math.isfinite()` to validate inputs**
   ```python
   if math.isfinite(x):
       result = safe_calculation(x)
   ```

6. **For exact integer results, check if float result is whole number**
   ```python
   result = math.sqrt(4)  # Returns 2.0
   if result == int(result):
       print("Perfect square!")
   ```

## Performance Considerations

1. **For integer exponentiation**, use integer arithmetic
   ```python
   x ** 2      # Faster for integers
   math.pow(x, 2)  # Always returns float
   ```

2. **In tight loops, minimize function calls**
   ```python
   # Better
   PI = math.pi
   E = math.e
   for i in range(1000000):
       result = i * PI + E
   ```

3. **Batch processing for large datasets**
   - Consider NumPy for array operations
   - More efficient than repeated math() calls

## Additional Resources

- [Python math module documentation](https://docs.python.org/3/library/math.html)
- [Mathematical constants and functions](https://en.wikipedia.org/wiki/Mathematics)
- Numerical computations with Python

---

*This documentation covers the mathematical operations demonstrated in the Python Features Explorer project.*
