# How to use 
Download the latest release put it in ...\whl\tkweb and load it using micropip (aka. pyodide)
```
                await pyodide.loadPackage("micropip");
                const micropip = pyodide.pyimport("micropip");
                await micropip.install(YOUR_WEBSITE_NAME\...\whl\tkweb\WHL_NAME.whl)
```
**DO __NOT__ USE FORM GITHUB DIREKTLY YOU __CAN AND WILL__ ENCOUNTER __A CORS 304__ ERROR**
