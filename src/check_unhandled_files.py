import os


class Checker():
    def __init__(self, upload_path: str, dest_path: str):
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        self.upload_path = upload_path
        self.dest_path = dest_path
        self.handled_history = r'handled_files.txt'
    
    def check_unhandled_files(self) -> list[str]:
        if not os.path.isfile(self.handled_history):
            with open(self.handled_history, 'w', encoding='utf-8') as f:
                f.write('')

        handled_files, unhandled_files = [], []
        with open(self.handled_history, 'r', encoding='utf-8') as f:
            handled_files = f.read().split('\n')
        for file in os.listdir(self.upload_path):
            if file not in handled_files:
                unhandled_files.append(file)
        
        return unhandled_files

    def update_handled_files(self, handled_files: list[str]) -> None:
        with open(self.handled_history, 'a', encoding='utf-8') as f:
            for file in handled_files:
                f.write(file + '\n')
    
    def reset_handled_files(self) -> None:
        with open(self.handled_history, 'w', encoding='utf-8') as f:
            f.write('')


if __name__ == "__main__":
    checker = Checker(r'./upload', r'./result')
    unhandled_files = checker.check_unhandled_files()
    print(unhandled_files)
    checker.update_handled_files(unhandled_files)
    # checker.reset_handled_files()
    # unhandled_files = checker.check_unhandled_files()
    # print(unhandled_files)