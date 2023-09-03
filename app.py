import asyncio
import random
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
from breadboard import breadboard
from max6675 import MAX6675, MAX6675Error
app = FastAPI()
# default example
app.cs_pin = 24
app.clock_pin = 23
app.data_pin1 = 22
#app.data_pin2 = 18
app.units = "f"
app.bb = breadboard(app.cs_pin, app.clock_pin)
app.thermocouple1 = MAX6675(app.clock_pin, app.data_pin1, app.units)
#app.thermocouple2 = MAX6675(app.clock_pin, app.data_pin2, app.units)

templates = Jinja2Templates(directory="templates")

connected_websockets = set()

@app.get("/")
async def index(request: Request):
    print("bruh")
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    print("websocket connected")
    try:
        while True:
            try:
                app.bb.wake()
                print("bread is awake")
                tc1 = app.thermocouple1.get()
                #tc2 = app.thermocouple2.get()
                app.bb.sleep()
            #number = random.randint(1, 100)
                for ws in connected_websockets:
                    await ws.send_text(str(tc1))
                await asyncio.sleep(1)
                
            except MAX6675Error as e:
                tc = "Error: "+ e.value
                running = False
                print("tc: {}".format(tc))
                await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    #set up pins and objects
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        app.bb.cleanup()
