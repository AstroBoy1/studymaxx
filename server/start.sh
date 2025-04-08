#!/bin/bash

# export FLASK_DEBUG=1
# export FLASK_ENV=development

# flask --app main run --port=5001
#!/bin/bash

export FLASK_ENV=production  # Set Flask to production mode

flask --app main run --host=0.0.0.0 --port=${PORT:-5000}  # Bind to 0.0.0.0 and use the $PORT variable