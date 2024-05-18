from pynput import mouse

class ScreenBoxSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.bbox = None
        
        self.listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        
    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                # Capture the initial coordinates on mouse button press
                self.start_x, self.start_y = x, y
                print(f"Mouse pressed at ({self.start_x}, {self.start_y})")
            else:
                # Capture the final coordinates on mouse button release
                self.end_x, self.end_y = x, y
                self.bbox = (self.start_x, self.start_y, self.end_x, self.end_y)
                print(f"Selection Box Coordinates: {self.bbox}")
                # Stop listener after selection
                return False

    def on_move(self, x, y):
        # if self.start_x is not None and self.start_y is not None:
        #     # Update coordinates while dragging (optional)
        #     print(f"Mouse dragged to ({x}, {y})")
        pass

    def start_selection(self):
        with self.listener as listener:
            listener.join()
        x1, y1, x2, y2 = self.bbox
        self.bbox = (min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2))
        return self.bbox

if __name__ == "__main__":
    selector = ScreenBoxSelector()
    bbox = selector.start_selection()
    print(f"Final bounding box: {bbox}")
