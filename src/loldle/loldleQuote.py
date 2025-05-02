from .loldleAPI import LoldleAPI


class LoldleQuote(LoldleAPI):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        print("Mode Citation:")
        super().start()
