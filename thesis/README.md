## Building instructions and requirements
The thesis is written in [Latex](https://www.latex-project.org/get/) and built with [cmake](https://cmake.org/)
with the help of [UseLATEX](https://gitlab.kitware.com/kmorel/UseLATEX).
Check that you have these installed. UseLATEX is a helper file which already exists in this project. You can
replace it if you want with the latest version. Then make a new folder inside this one and run cmake. Example:
```bash
mkdir build
cd build/
cmake ../
make
```

## Useful links
Beside reading the documentation of the importated packages, you should check out these websites:
* [Detexify](http://detexify.kirelabs.org/classify.html) good for finding math symbols by drawing them
