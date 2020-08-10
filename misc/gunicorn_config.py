import os

workers = 2
timeout = 60

# Use the port designed by Heroku
bind = '0.0.0.0:' + os.environ.get("PORT", "5001")
