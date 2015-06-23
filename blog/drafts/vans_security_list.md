Title: Van Lindberg's List of Security Practices
Category: Python
Tags: python, security
Author: Christian Long
Date: 2015-06-23 13:35
Summary: A quick post to gather a list of security best practices that Van Lindberg tweeted.




[Van Lindberg](https://twitter.com/VanL), chair of the [Python Software Foundation](https://www.python.org/psf/), recently tweeted [1](https://twitter.com/VanL/status/613395093165191168) [2](https://twitter.com/VanL/status/613395274824744960) [3](https://twitter.com/VanL/status/613395987646644226) [4](https://twitter.com/VanL/status/613397346550812672) [5](https://twitter.com/VanL/status/613397542491983873) a list of security best practices. For my information and future reference, I'm gathering them here.

1. Thorough negative testing. Cause failures with test cases.
2. Fuzz with address checking and standard alloc
3. Compiling with address checking and standard memory alloc
4. Focused manual spotcheck validation of fields
5. Fuzzing w/ output examination
6. Context-sensitive source code analysis
7. Multi-implementation tests
8. Aggressive, not compiled out runtime assertions
9. Implementations in safer languages
10. Static analysis
11. Thorough human review/audit
12. Formal methods
Use more than 1.
