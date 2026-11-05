# Lab 5: Static Code Analysis

## Project
**Project:** Courier and Parcel Tracking System  
**File analyzed:** `parcel_tracker.py`  
**Tools:** Pylint, Bandit, Flake8

## Issues Identified and Resolved

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Mutable default argument | Code quality / potential bug | 11 | The function used `history=[]`, causing the same list to be shared across calls that omit the argument. | Changed the default to `None` and initialized a new list inside the function. |
| Insecure temporary filename | Security, Medium | 50 | `tempfile.mktemp()` generates a filename without securely creating the file. | Replaced it with `tempfile.NamedTemporaryFile()` using `delete=False`. |
| Shell command execution | Security, High | 55 | The original ping function used `shell=True` and concatenated the address into a command string, creating a potential command-injection risk. | Removed the unused ping helper and its `subprocess` import. |
| Insecure OTP generation | Security, Low | 72 | The original program used `random.randint()` for a delivery OTP. The standard `random` module is unsuitable for security-sensitive randomness. | Replaced it with `secrets.randbelow()`. |
| Broad exception handling | Code quality | 37 | Catching `Exception` can hide unexpected errors. | Used `parcels.get()` to handle an unknown tracking ID directly. |
| Non-standard naming | Code quality | Multiple | Function names and variables did not follow Python's `snake_case` convention. | Renamed functions and variables to follow conventional Python naming. |
| Missing documentation | Code quality | Multiple | The module and functions lacked docstrings. | Added module and function docstrings. |
| Spacing violations | Formatting | 28, 74 | Missing spaces around operators and after commas violated PEP 8 formatting. | Corrected spacing. |
| Inline comment spacing | Formatting | 71 | The original inline comment did not have the required spacing. | Corrected the spacing and removed the inline comment. |
| Missing blank lines | Formatting | 75 | The file did not have the required blank lines before the top-level function call. | Added the standard main guard and appropriate spacing. |

## Verification Results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.91/10 | 10.00/10 |
| Bandit | 4 findings: 1 High, 1 Medium, 2 Low | No findings |
| Flake8 | 4 formatting violations | No violations |

## Conclusion

Static analysis identified issues affecting code quality, security, naming conventions, and formatting. The program was updated to address the findings, and all three tools were rerun against the final version. Pylint achieved a score of 10/10, Bandit reported no findings, and Flake8 reported no formatting violations.