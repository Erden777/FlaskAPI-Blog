import os
from importlib import import_module

def import_modules(modules_dir: str, exclude=[]) -> None:
    for dir_path, dir_names, file_names in os.walk(modules_dir):
        for file_name in file_names:
            if file_name.endswith("py") and not file_name in exclude:
                file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
                module_name = file_path_wo_ext.replace(os.sep, ".")
                import_module(module_name)