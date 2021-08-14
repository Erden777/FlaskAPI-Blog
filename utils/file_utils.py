import os, shutil
from importlib import import_module
from flask import current_app
from werkzeug.utils import secure_filename

def get_modules(dir_path, file_name):
    file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
    module_name = file_path_wo_ext.replace(os.sep, ".")
    import_module(module_name)

def import_modules(modules_dir: str, exclude=[], include=[]) -> None:
    for dir_path, dir_names, file_names in os.walk(modules_dir):
        for file_name in file_names:
            if not include:
                if file_name.endswith("py") and not file_name in exclude:
                    get_modules(dir_path, file_name)
            else:
                if file_name.endswith("py") and file_name in include:
                    get_modules(dir_path, file_name)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def clear_dir(directory):
    for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Details: %s' % (file_path, e))

# def upload_files(files, dir='', clear=False):
#     files_path = []

#     file_dir = os.path.join(current_app.config['UPLOAD_DIR'], dir)

#     if not os.path.exists(file_dir):
#         os.makedirs(file_dir)

#     if clear == True:
#         clear_dir(file_dir)

#     for file in files:
#         if file.filename != '' and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_ext = '.' + file.filename.split('.').pop().lower()
#             filename = random_string() + file_ext

#             file_path = os.path.join(file_dir, filename)
#             common_prefix = os.path.commonprefix([current_app.config['BASE_DIR'], os.path.join(file_dir, filename)])
            
#             files_path.append('/' + os.path.relpath(file_path, common_prefix))
#             file.save(file_path)         

#     return files_path