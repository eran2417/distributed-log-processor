import os

# Sample Log Messages
LOG_MESSAGES = {
    "INFO": [
        "User logged in successfully",
        "Page loaded in 0.2 seconds",
        "Database connection established",
        "Cache refreshed successfully",
        "API request completed"
    ],
    "WARNING": [
        "High memory usage detected",
        "API response time exceeding threshold",
        "Database connection pool running low",
        "Retry attempt for failed operation",
        "Cache miss rate increasing"
    ],
    "ERROR": [
        "Failed to connect to database",
        "API request timeout",
        "Invalid user credentials",
        "Processing error in data pipeline",
        "Out of memory error"
    ],
    "DEBUG": [
        "Function X called with parameters Y",
        "SQL query execution details",
        "Cache lookup performed",
        "Request headers processed",
        "Internal state transition"
    ]
}
LOG_SERVICES = [
    "AUTH_SERVICE",
    "PAYMENT_SERVICE",
    "USER_SERVICE",
    "ORDER_SERVICE",
    "INVENTORY_SERVICE"
]


# Default configuration values
DEFAULT_CONFIG = {
    "LOG_FORMAT": "text",
    "LOG_RATE": 2,  # Logs per second
    "LOG_TYPES": ["INFO", "WARNING", "ERROR", "DEBUG"],
    "LOG_DISTRIBUTION": {
        "INFO": 70,     # 70% of logs will be INFO
        "WARNING": 20,  # 20% of logs will be WARNING
        "ERROR": 5,     # 5% of logs will be ERROR
        "DEBUG": 5      # 5% of logs will be DEBUG
    },
    "OUTPUT_FILE": "/logs/generated_logs.log",
    "CONSOLE_OUTPUT": True,
    "ENABLE_BURSTS": True,
    "BURSTS_FREQUENCY": 20,  # Every 20 seconds
    "BURSTS_DURATION": 2,    # Bursts last for 2 seconds
    "BURSTS_MULTIPLIER": 5   # 5 times the normal rate
}

# Load configuration from environment variables
config = {
    "LOG_FORMAT": os.environ.get("LOG_FORMAT", DEFAULT_CONFIG["LOG_FORMAT"]),
    "LOG_RATE": int(os.environ.get("LOG_RATE", DEFAULT_CONFIG["LOG_RATE"])),
    "LOG_TYPES": os.environ.get("LOG_TYPES", ",".join(DEFAULT_CONFIG["LOG_TYPES"])).split(","),
    "OUTPUT_FILE": os.environ.get("OUTPUT_FILE", DEFAULT_CONFIG["OUTPUT_FILE"]),
    "LOG_MESSAGES": LOG_MESSAGES,
    "LOG_SERVICES": LOG_SERVICES,
    "CONSOLE_OUTPUT": os.environ.get("CONSOLE_OUTPUT", str(DEFAULT_CONFIG["CONSOLE_OUTPUT"])).lower() == "true",
    "ENABLE_BURSTS": os.environ.get("ENABLE_BURSTS", str(DEFAULT_CONFIG["ENABLE_BURSTS"])).lower() == "true",
    "BURSTS_FREQUENCY": int(os.environ.get("BURSTS_FREQUENCY", DEFAULT_CONFIG["BURSTS_FREQUENCY"])),
    "BURSTS_DURATION": int(os.environ.get("BURSTS_DURATION", DEFAULT_CONFIG["BURSTS_DURATION"])),
    "BURSTS_MULTIPLIER": int(os.environ.get("BURSTS_MULTIPLIER", DEFAULT_CONFIG["BURSTS_MULTIPLIER"]))
}

# Set log distribution
LOG_DISTRIBUTION = {}
for log_type in config["LOG_TYPES"]:
    env_key = f"LOG_DIST_{log_type}"
    if log_type in DEFAULT_CONFIG["LOG_DISTRIBUTION"]:
        LOG_DISTRIBUTION[log_type] = int(os.environ.get(env_key, DEFAULT_CONFIG["LOG_DISTRIBUTION"][log_type]))
    else:
        LOG_DISTRIBUTION[log_type] = int(os.environ.get(env_key, 0))

config["LOG_DISTRIBUTION"] = LOG_DISTRIBUTION
