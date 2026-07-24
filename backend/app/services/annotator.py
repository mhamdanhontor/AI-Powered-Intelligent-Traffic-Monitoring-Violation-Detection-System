import cv2


class FrameAnnotator:

    @staticmethod
    def draw(results, frame, line_y):

        annotated = results[0].plot()

        cv2.line(

            annotated,

            (0, line_y),

            (annotated.shape[1], line_y),

            (0, 255, 255),

            3

        )

        return annotated