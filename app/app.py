# from os.path import join, dirname, abspath, exists
# from flask import Flask
# from dotenv import load_dotenv

# def create_app():
#     base_dir = dirname(dirname(abspath(__file__)))
#     config_file = join(base_dir, 'config.py')
#     env_file = join(base_dir, '.env')
#     app = Flask(    
#         __name__,
#         instance_relative_config=False,
#         root_path=base_dir,
#     )

#     if exists(env_file):
#         app.config.from_pyfile(config_file)
#         load_dotenv(dotenv_path=env_file)

#     return app
