# Lab 5: Static Code Analysis Reflection

## 1. What is the purpose of static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding-standard violations. It helps developers discover problems early in development. In this lab, Pylint, Bandit, and Flake8 examined different aspects of the parcel-tracking program.

## 2. What did the three tools identify?

Pylint identified code-quality problems, including a mutable default argument, overly broad exception handling, inconsistent naming, and missing documentation. Bandit identified security concerns involving temporary-file creation, shell command execution, and OTP generation. Flake8 identified formatting violations involving whitespace and blank lines.

## 3. How did the fixes improve the program?

The fixes improved the code's readability, maintainability, and security. The mutable default argument was replaced with `None`, the broad exception handling was removed, the temporary-file implementation was made safer, and the OTP generator was changed to use the `secrets` module. Naming conventions and formatting were also corrected.

## 4. What did you learn from this lab?

I learned that a program can execute successfully while still containing security and code-quality problems. Using multiple static-analysis tools provides different perspectives on the same source code. Rerunning the tools after making changes provides measurable evidence that the identified problems have been addressed.