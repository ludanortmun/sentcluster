import uvicorn
from sentcluster.http.api import app

if __name__ == "__main__":
    uvicorn.run("sentcluster.http.api:app", host="0.0.0.0", port=8000, reload=True)
