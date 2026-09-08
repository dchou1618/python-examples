# python examples
Practice with Jupyter Notebook, Python, and Algorithms

#### Review 
* Python defines a default constructor in the class, which exists regardless of created constructor unlike Java.
* Python has duck typing so it doesn't enforce type hints at runtime. It only cares about if the object has existing methods. Java is statically typed and enforces strict inheritance rules at compile time, so a parent object passed into an argument expecting a child class will raise a compile time error.
* Python has mutable default arguments, so use None on the list instead.
* In Python, modifying a list cannot be done while iterating over it.
* Python has double equal sign that checks for value equality. `is` confirms if two objects/variables are the same, so:
    ```python
    a = 256
    b = 256
    print(a is b)
    ```
    * The print statement returns True because Python optimizes by caching small values -5 to 256 and short strings into memory. However, if the two variables were assigned to 257, they are not equal.
    * Defining a mutable value in python class body updates the value to be shared by all instances of the class.