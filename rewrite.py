import os

file_path = 'c:/Users/catar/Downloads/multi-agent-main/IAG-system-main/agentes_animais/web/server.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

old_syspath = "import sys\nsys.path.insert(0, '/workspace')"
new_syspath = "import os\nimport sys\ncurrent_dir = os.path.dirname(os.path.abspath(__file__))\nparent_dir = os.path.dirname(os.path.dirname(current_dir))\nsys.path.insert(0, parent_dir)"
code = code.replace(old_syspath, new_syspath)

code = code.replace('directory="/workspace/agentes_animais/web"', 'directory=current_dir')
code = code.replace('open("/workspace/agentes_animais/web/index.html",', 'open(os.path.join(current_dir, "index.html"),')

code = code.replace('agent.animal_type', 'agent.animal_name')
code = code.replace('agent.group_factor', 'agent.adaptation_group')
code = code.replace('agent.solo_factor', 'agent.adaptation_solo')
code = code.replace('agent.skills', 'agent.characteristics')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Rewrite complete!')
