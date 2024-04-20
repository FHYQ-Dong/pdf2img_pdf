import check_unhandled_files, pdf2img_pdf
import os


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    upload_path, result_path = r'../upload', r'../result'

    checker = check_unhandled_files.Checker(upload_path, result_path)
    unhandled_files = checker.check_unhandled_files()
    for file in unhandled_files:
        upload_file = os.path.join(upload_path, file)
        result_file = os.path.join(result_path, file)
        pdf2img_pdf.pdf2img_pdf(upload_file, result_file, 2)
    checker.update_handled_files(unhandled_files)
