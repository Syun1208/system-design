import redis

try:
    # Use the correct Redis port (6379 instead of 1201)
    r = redis.Redis(host='localhost', port=6379, health_check_interval=30)
    response = r.ping()
    
    # Set a key-value pair in Redis
    r.set('my_key', 'my_value')

    # Retrieve the value by key
    value = r.get('my_key')
    print(f"The value for 'my_key' is: {value.decode('utf-8')}")
    
    if response:
        print("Connected to Redis!")
except redis.ConnectionError as e:
    print("Failed to connect to Redis:", e)

r.close()
