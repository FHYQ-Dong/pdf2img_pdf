import check_unhandled_files, pdf2img_pdf
import os, json


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    upload_path, result_path = r'../upload', r'../result'
    workflow_info_file = r'../src/workflow_info.json'
    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    workflow_info = {
        'title': '',
        'body': '',
        'tag': 0,
        'zip-file': '',
        'publish': False
    }
    if not os.path.isfile(workflow_info_file):
        with open(workflow_info_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(workflow_info, ensure_ascii=False, indent=4))

    with open(workflow_info_file, 'r', encoding='utf-8') as f:
        workflow_info = json.load(f)

    checker = check_unhandled_files.Checker(upload_path, result_path)
    unhandled_files = checker.check_unhandled_files()
    for file in unhandled_files:
        upload_file = os.path.join(upload_path, file)
        result_file = os.path.join(result_path, file)
        pdf2img_pdf.pdf2img_pdf(upload_file, result_file, 2)
    checker.update_handled_files(unhandled_files)

    if unhandled_files != []:
        workflow_info['title'] = unhandled_files[0]
        workflow_info['body'] = '\n'.join(unhandled_files)
        workflow_info['tag'] = int(workflow_info['tag']) + 1
        workflow_info['zip-file'] = r'./result/result.zip'
        workflow_info['publish'] = True
    else:
        workflow_info['title'] = ''
        workflow_info['body'] = ''
        workflow_info['zip-file'] = ''
        workflow_info['publish'] = False
    
    with open(workflow_info_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(workflow_info, ensure_ascii=False, indent=4))
    os.system(r'zip -r ../result/result.zip ../result/*')