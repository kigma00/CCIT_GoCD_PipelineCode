import yaml

# 변경사항을 기반으로 YAML 데이터 생성
data = {
    'pipeline': {
        'name': 'example-pipeline',
        'trigger': 'commit-change',
        'jobs': [
            {
                'name': 'build',
                'steps': ['echo "Building project..."']
            },
            {
                'name': 'test',
                'steps': ['echo "Running tests..."']
            }
        ]
    }
}

# YAML 파일 생성
with open('pipeline_config.yaml', 'w') as file:
    yaml.dump(data, file, sort_keys=False)

print("YAML file generated successfully.")
