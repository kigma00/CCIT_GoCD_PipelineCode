import yaml

# YAML 파일 읽기
with open('pipeline_config.yaml', 'r') as file:
    pipeline_config = yaml.safe_load(file)

# 파이프라인 정보 출력
pipeline_name = pipeline_config['pipeline']['name']
print(f"Pipeline: {pipeline_name}")

# 각 작업에 대한 정보 출력
for job in pipeline_config['pipeline']['jobs']:
    print(f"Job: {job['name']}")
    for step in job['steps']:
        print(f"Step: {step}")
