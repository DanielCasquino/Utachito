import time

import cv2

from utachito import (
    CameraService,
    YoloService,
    MemoryService,
    FsmService,
)

cameraService = CameraService()
yoloService = YoloService()
memoryService = MemoryService(yoloService)
fsmService = FsmService(memoryService)

target_fps = 8
frame_delay = 1 / target_fps
show_preview = True
elapsed_time = 0.10

cameraService.start()

while True:
    start_time = time.time()

    photo = cameraService.get_photo()
    results = yoloService.analyze_photo(photo)
    memoryService.remember(results, photo, start_time)
    fsmService.think(photo, elapsed_time)

    # if show_preview:
        # annotated_frame = results[0].plot()
        # cv2.imshow("Camera", annotated_frame)

    elapsed_time = time.time() - start_time
    sleep_time = frame_delay - elapsed_time
    print("Elapsed time: ", elapsed_time)
    print("Sleep time: ", sleep_time)


    if sleep_time > 0:
        time.sleep(sleep_time)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
