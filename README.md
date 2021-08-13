# PyWebServer
A bare-bones web server written with Python.

**Note:** This web server is tested and working with Python 3.7 on Windows 10. I wouldn't advise using this in any sort of production capacity. There are probably critical bugs in this application.

## How does it work?

PyWebServer utilizes sockets to accept connections over TCP. As of right now, PyWebServer is multi-processed application capable of asynchronously parsing basic HTTP GET requests and responding with the requested resource(s), if available.
