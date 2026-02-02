import os
import time
import sys
from log_generator import LogGenerator
from config import config


def main():
    
    # Read configuration from environment variables
    print("Starting log generator with configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Create and start generator
    generator = LogGenerator(config=config)

    duration = None
    if len(sys.argv) > 1:
        try:
            duration = float(sys.argv[1])
            print(f"Generator will run for {duration} seconds")
        except ValueError:
            print(f"Invalid duration: {sys.argv[1]}")
    generator.start(duration=duration)


if __name__ == "__main__":
    main()