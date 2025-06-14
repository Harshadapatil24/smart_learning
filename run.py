#!/usr/bin/env python
"""from simple_app import app

if __name__ == '__main__':
    port = 3000
    print(f"Starting server at http://localhost:{port}")
    app.run(host='localhost', port=port, debug=True) """

from simple_app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT from the environment
    print(f"Starting server at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
