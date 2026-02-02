import time
import time
import random
import os
import json
import csv
import io
from datetime import datetime


class LogGenerator:
    """Generate and send logs at a configurable rate."""
    
    def __init__(self, config):
        self.config = config
        self.ensure_log_directory()

    def ensure_log_directory(self):
        log_dir = os.path.dirname(self.config["OUTPUT_FILE"])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    
    def generate_log(self):
        """Generate a random log entry message based on configured types."""
        log_type = self.select_log_type()
        service = self.select_log_service()
        messages = self.config.get("LOG_MESSAGES", {})
        if log_type in messages:
            message = random.choice(messages[log_type])
        else:
            message = f"Sample log message for {log_type}"

        timestamp = datetime.now().isoformat()
        request_id = f"req-{int(time.time())}-{random.randint(1000, 9999)}"
        user_id = f"user-{random.randint(1000, 9999)}"
        duration = random.randint(10, 500)

        log_format = self.config.get("LOG_FORMAT").lower()

        if log_format == "json":
            log_data = {
                "timestamp": timestamp,
                "level": log_type,
                "service": service,
                "user_id": user_id,
                "request_id": request_id,
                "duration_ms": duration,
                "message": message
            }
            return json.dumps(log_data)
        elif log_format == "csv":
            output = io.StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow([timestamp, log_type, service, request_id, user_id, duration, message])
            return output.getvalue().strip()
        else:
            # Default to text
            return f"{timestamp} [{log_type}] [{service}] [{request_id}] [{user_id}]  ({duration}ms) : {message}"
   
    
    def select_log_type(self):
        """Select a log type according to configured distribution."""

        dist = self.config.get('LOG_DISTRIBUTION')

        types = list(dist.keys())
        weights = [int(dist.get(t, 0)) for t in types]

        # Use random.choices with weights
        return random.choices(types, weights=weights, k=1)[0]
    
    def select_log_service(self):
        """Select a log service randomly from configured services."""
        services = self.config.get("LOG_SERVICES")
        return random.choice(services)
       
    
    def write_log_to_file(self, log_entry):
        """Write a log entry to the configured outputs."""
        # Write to file if configured
        output_file = self.config.get("OUTPUT_FILE")
        if output_file:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")

        # Write to console if configured
        if self.config.get("CONSOLE_OUTPUT"):
            print(log_entry)

    
    def start(self, duration=None):
        """Start generating and writing logs.
        
        Args:
            duration (int): Duration in seconds (None for infinite)
        """
       
        log_rate = self.config.get("LOG_RATE", 1)
        interval = 1.0 / log_rate if log_rate > 0 else 1.0
        if(self.config.get("ENABLE_BURSTS")):
            burst_freq = self.config.get("BURSTS_FREQUENCY", 10)
            burst_duration = self.config.get("BURSTS_DURATION", 2)
            burst_multiplier = self.config.get("BURSTS_MULTIPLIER", 5)
            # Adjust log rate for bursts
            burst_log_rate = log_rate * burst_multiplier
            burst_interval = 1.0 / burst_log_rate if burst_log_rate > 0 else 1.0
            next_burst_time = time.time() + burst_freq;
        print(f"Starting log generator at {log_rate} logs/second...")
        
        try:
            start_time = time.time()
            log_count = 0
            while True:
                current_time = time.time()
                # Check if duration limit reached
                if duration and (current_time - start_time) >= duration:
                    print(f"\nGeneration duration ({duration}s) completed.")
                    break
                if(current_time >= next_burst_time):
                    print(f"\n--- Burst mode activated: {burst_log_rate} logs/second for {burst_duration} seconds ---")
                    burst_end_time = current_time + burst_duration
                    while current_time < burst_end_time:
                        log_entry = self.generate_log()
                        self.write_log_to_file(log_entry)
                        log_count += 1
                        time.sleep(burst_interval)
                        current_time = time.time()
                    print(f"--- Burst mode ended ---\n")
                    next_burst_time = current_time + burst_freq                
                # Generate and write log
                log_entry = self.generate_log()
                self.write_log_to_file(log_entry)
                log_count += 1
                
                # Sleep based on configured rate
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\nLog generator stopped. Generated {log_count} logs.")

