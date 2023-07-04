import asyncio
import random
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

app = FastAPI()


templates = Jinja2Templates(directory="templates")

connected_websockets = set()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    try:
        while True:
            try:
                tc1 = thermocouple1.get()
                tc2 = thermocouple2.get()
            #number = random.randint(1, 100)
                for ws in connected_websockets:
                    await ws.send_text(str(number))
                await asyncio.sleep(1)
                
            except MAX6675Error as e:
                tc = "Error: "+ e.value
                running = False
                print("tc: {}".format(tc))
            
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    #set up pins and objects
    # default example
    cs_pin = 24
    clock_pin = 23
    data_pin1 = 22
    data_pin2 = 18
    units = "f"
    bb = breadboard(cs_pin, clock_pin)
    thermocouple1 = MAX6675(clock_pin, data_pin1, units)
    thermocouple2 = MAX6675(clock_pin, data_pin2, units)
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        breadboard.cleanup()
