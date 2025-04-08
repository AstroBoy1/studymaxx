#!/bin/bash

# export FLASK_DEBUG=1
# export FLASK_ENV=development

# flask --app main run --port=5001
export FLASK_ENV=production  # Set Flask to production mode

flask --app main run --port=${PORT:-5000}  # Use the $PORT variable or default to 5000
