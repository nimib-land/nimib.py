### implementing nbcode

- relevant to implement `nb.code`: https://github.com/streamlit/streamlit/blob/1.25.0/lib/streamlit/echo.py
- code explained: https://discuss.streamlit.io/t/how-does-st-echo-work/48011/3
- capturing code: https://stackoverflow.com/a/16571630

### implementing pyscript

- I would need a context manager that does not yield, maybe not possible?
   - https://discuss.python.org/t/preventing-yield-inside-certain-context-managers/1091/18
   - https://stackoverflow.com/questions/34519706/context-manager-without-yield
- as a workaround I can raise an error
- code is full of workarounds
- adapting Mousey mousey by ntoll https://pyscript.com/@3fd38942-d35c-4bf6-9b8a-37cec059f572/490a83cc-d1d2-4dad-8a74-c385343b010c/latest