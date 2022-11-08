# IfcOpenShell WASM

Live version: https://ifcopenshell.github.io/wasm-preview/

This is a technological preview of an IfcOpenShell WASM python module for use in [pyodide](https://pyodide.org/en/stable/). It uses [emscripten](https://emscripten.org/) to compile the C/C++ (of the python interpreter, IfcOpenShell and its dependencies respectively) into a WebAssembly (WASM) module. WebAssembly can be used in the browser or other JavaScript runtimes such as NodeJS.

## Approach

This approach of supporting IFC within the browser is rather heavy as it depends on a python interpreter loading the wasm-compiled monolithic IfcOpenShell wheel on demand. But nevertheless, we see this as the most powerful approach of enabling IfcOpenShell in the browser.

Over time, Python code has surpassed C++ as the predominant language in IfcOpenShell and has become the defacto standard for the IfcOpenShell API. We wouldn't want browser-based usage to require duplicating this powerful set of APIs.

<img src="https://user-images.githubusercontent.com/1096535/200540038-7cfc6a1a-2855-43a4-a4c2-9a3dea3acbf7.png" width=500>

Wrapping the full IfcOpenShell-python module results in a feature rich module, that makes for example, IFC validation, visualization, but also **authoring** a breeze because any pre-existing pure python module can be leveraged.

<img src="https://user-images.githubusercontent.com/1096535/200540631-8832d6d2-e864-44a6-bd6e-afe37e4a8d2d.png" width=500>

## Usage

### Pyodide proxy objects

Allows direct usage of python objects in JavaScript code.

Example: https://github.com/IfcOpenShell/wasm-preview/blob/master/index.html#L99-L101

### Python code evaluation by Pyodide

Allows running actual python code with the ability for JavaScript to easily reflect on global variables.

Example: https://github.com/IfcOpenShell/wasm-preview/blob/master/index.html#L114-L117

### In-line python code using PyScript

Allows running inline python code in HTML script tags

## Limitations

- Performance of loading and running code is not optimal.
- C++ exception handling in the IfcOpenShell dependencies seems to cause issues in WASM.

## Future work

The overall IfcOpenShell roadmap of modularizing the geometry libraries, providing alternative implementations (CGAL, Eigen) and providing a more plug-in like interface will alleviate most of the issues WASM-IfcOpenShell users will experience as emscripten can load shared libraries on demand.

Stay tuned!
