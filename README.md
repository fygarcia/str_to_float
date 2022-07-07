# str_to_float(str)
"function tries to convert a string into a float, replacing and fixing comma and dots as thousand and decimal separators"

This is a simple example of a function that receives one input string parameter and tries to convert it into a float.  
Example:

```
$ str_to_float('1.000,00') 
>>> 1000.00
```

The _str_to_float.py_ file also has a test function < `test_str_to_float(func)` >, which loops through a hardcoded dictionary of possible use cases and its expected results.  
Test inputs are _.keys_ of this tdd dictionary, and the expected results are _.values_ of this dictionary.[^1]

The `test_str_to_float(func)` will print to the console each test result for debugging.


[^1]:  This piece of code was developed using the TDD Test Driven Development methodology.  
First, I designed the test function that would test de dicitonary of inputs and expected results.  
Then, I coded the str_to_float function, observing its results on the go.
