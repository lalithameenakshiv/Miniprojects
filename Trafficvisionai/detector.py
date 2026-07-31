import cv2
from ultralytics import YOLO
from collections import defaultdict
import os


# COCO vehicle classes
VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


def get_model_path(model_name="yolov8n"):
    base = f"models/{model_name}.pt"
    if os.path.exists(base):
        return base
    return "models/yolov8n.pt"


class VehicleDetector:

    def __init__(self, model_name="yolov8n", conf=0.4, iou=0.45, max_det=200):
        self.vehicle_counts = defaultdict(int)
        self.conf = conf
        self.iou = iou
        self.max_det = max_det
        self.model_path = get_model_path(model_name)
        self.model = YOLO(self.model_path)


    def process_video(self, input_video, output_video):

        cap = cv2.VideoCapture(input_video)


        if not cap.isOpened():
            raise Exception("Cannot open video file")


        width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )


        if fps == 0:
            fps = 30


        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )


        writer = cv2.VideoWriter(
            output_video,
            fourcc,
            fps,
            (width, height)
        )


        while True:


            ret, frame = cap.read()


            if not ret:
                break



            # YOLO Detection

            results = self.model(
                frame,
                verbose=False,
                conf=self.conf,
                iou=self.iou,
                max_det=self.max_det
            )[0]



            frame_counts = defaultdict(int)



            for box in results.boxes:


                cls_id = int(
                    box.cls[0]
                )


                if cls_id not in VEHICLE_CLASSES:
                    continue



                vehicle_name = VEHICLE_CLASSES[cls_id]


                frame_counts[vehicle_name] += 1


                self.vehicle_counts[vehicle_name] += 1



                # Bounding box

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                confidence = float(
                    box.conf[0]
                )



                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0,255,0),
                    2
                )


                label = (
                    f"{vehicle_name} "
                    f"{confidence:.2f}"
                )


                cv2.putText(
                    frame,
                    label,
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )



            # Display information

            y = 40


            cv2.putText(
                frame,
                "Traffic Vision AI",
                (20,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2
            )


            y += 40


            total_frame = 0


            for vehicle in [
                "Car",
                "Motorcycle",
                "Bus",
                "Truck"
            ]:


                count = frame_counts[vehicle]

                total_frame += count


                cv2.putText(
                    frame,
                    f"{vehicle}: {count}",
                    (20,y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,255),
                    2
                )


                y += 30



            cv2.putText(
                frame,
                f"Vehicles: {total_frame}",
                (20,y+10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,255),
                2
            )



            writer.write(frame)



        cap.release()
        writer.release()



        return {

            "Car":
            self.vehicle_counts["Car"],

            "Motorcycle":
            self.vehicle_counts["Motorcycle"],

            "Bus":
            self.vehicle_counts["Bus"],

            "Truck":
            self.vehicle_counts["Truck"],

            "Total":
            sum(self.vehicle_counts.values()),

            "Output Video":
            output_video
        }