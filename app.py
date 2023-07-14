from server import create_app
import redis
from server.config import redis_host, redis_port, redis_db

app = create_app()

if __name__ == "__main__":
    app.redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    try:
        # app.run(debug=True)
        app.run(debug=True, host='0.0.0.0')
    finally:
        app.redis_conn.close()
