import pygame
import time
from clientmods import *
import asyncio




 
async def Link(stream_found_event):
    global stream_url
    global matrix
    
    bufor_matrix = [0,0,0,0]
    try:
        connection.connect()
        stream_url = 'Dupa'
        stream_found_event.set()
        while True:
            if bufor_matrix != matrix:
                bufor_matrix = matrix
                connection.send_data(bufor_matrix)
            
            await asyncio.sleep(0)

    except ConnectionRefusedError:
        print("Server refused the connection")
    except TimeoutError:
        print("Connection timeout")
    except ConnectionAbortedError:
        print("Server closed connection")


async def Player(stream_found_event):
    global stream_url
    global matrix
    await stream_found_event.wait()
    window = Window()

    timer = time.time()
    fps_set = window.camera.get(5)
    while True:
        await asyncio.sleep(0)
        fps_timer = time.time()
        if(time.time() - timer > 1):
            window.Render_ping()
            timer = time.time()

        window.Play()
        pygame.display.update()

        if (time.time()-fps_timer) < (1/fps_set):
            time.sleep((1/fps_set)-(time.time()-fps_timer))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception()
            
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.JOYAXISMOTION:
                matrix = to_matrix(read_event(event))
                





stream_url = None
matrix = []

async def main():
    pygame.init()
    stream_found_event = asyncio.Event()
    await asyncio.gather(Player(stream_found_event), Link(stream_found_event))


steering = Control_device()
connection = Client()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except (KeyboardInterrupt, Exception) as e:
    print(e)
    raise(e)
    pass
finally:
    print('Ending program')
    connection.__del__()