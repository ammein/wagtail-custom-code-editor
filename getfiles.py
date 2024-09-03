import glob
import re

modes = glob.glob("wagtail_custom_code_editor/static/wagtail_custom_code_editor/ace/snippets/*")
final_mode = []
for mode in modes:
    final_mode.append(re.sub(r'.*[\\/]([^.]+)', r'\1', mode))

extensions = glob.glob("wagtail_custom_code_editor/static/wagtail_custom_code_editor/ace/ext-*")
final_extension = []
for extension in extensions:
    final_extension.append(re.sub(r'.*[\\/]([^.]+)', r'\1', extension))
workers = glob.glob("wagtail_custom_code_editor/static/wagtail_custom_code_editor/ace/worker-*")
final_worker = []
for worker in workers:
    final_worker.append(re.sub(r'.*[\\/]([^.]+)', r'\1', worker))

with open('wagtail_custom_code_editor/files.py', 'w') as f:
    f.writelines([
        re.sub(r'^MODES = *', 'MODES = ', 'MODES = {}'.format(final_mode.__str__())),
        "\n" + re.sub(r'^EXTENSIONS = *', 'EXTENSIONS = ', 'EXTENSIONS = {}'.format(final_extension.__str__())),
        "\n" + re.sub(r'^WORKERS = *', 'WORKERS = ', 'WORKERS = {}'.format(final_worker.__str__()))
    ])
    f.close()
