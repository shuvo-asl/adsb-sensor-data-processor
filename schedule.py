from bootstrap.bootstrap import app
from celery import Celery
import redis
import requests
from models.Position import Position
# Add Redis URL configurations
app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

# Connect Redis db
redis_db = redis.Redis(
      host="redis", port="6379", db=1, charset="utf-8", decode_responses=True
  )

# Initialize timer in Redis
redis_db.mset({"minute": 0, "second": 0})

# Add periodic tasks
celery_beat_schedule = {
      # "time_scheduler": {
	  # "task": "schedule.timer",
	  # "schedule": 1.0,# Run every second
      # }
     "sensor_scheduler": {
	  "task": "schedule.data_pulling",
	  "schedule": 1.0,# Run every second
      }
  }

# Initialize Celery and update its config
celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)

@celery.task
def timer():
    second_counter = int(redis_db.get("second")) + 1
    if second_counter >= 59:
	    # Reset the counter
	    redis_db.set("second", 0)
	    # Increment the minute
	    redis_db.set("minute", int(redis_db.get("minute")) + 1)
    else:
	    # Increment the second
	    redis_db.set("second", second_counter)

@celery.task
def data_pulling():
    unique_data = []
    khulna = requests.get("http://192.168.201.3/aircraftlist.json").json();
    dhaka = requests.get("http://192.168.30.27/aircraftlist.json").json();

    # Combine the JSON objects into a single list
    data_list = []
    data_list.extend(khulna)
    data_list.extend(dhaka)
    hex_set = set()

    for item in data_list:
        hex_value = item['hex']
        if hex_value not in hex_set:
            position = Position.getPositionByUniqueCode(hex_value);
            if position:
                position.lat = item['lat']
                position.lon = item['lon']
                position.alt = item['alt']
                position.speed = item['spd']
            else:
                position = Position(**{
                    "unique_code": hex_value,
                    "lat": item['lat'],
                    "lon": item['lon'],
                    "alt": item['alt'],
                    "speed": item['spd']
                });

            position.save();
            hex_set.add(hex_value)
            unique_data.append(item)
    print("Sensor Data Pulled & Stored.",unique_data)

