uv remove torch
uv export --format requirements.txt --no-emit-workspace -o docker_requirements.txt
uv add torch