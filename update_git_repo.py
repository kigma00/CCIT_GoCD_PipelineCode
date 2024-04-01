import requests
import json
import base64

# GitHub 설정
owner = 'kigma00'  # GitHub 사용자 이름
repo = 'CCIT_GoCD_PipelineCode'  # GitHub 리포지토리 이름
path = 'CCIT_GoCD_PipelineCode.yaml'  # 생성하거나 수정할 파일의 경로
token = '{your_token}'  # GitHub Personal Access Token

# YAML 파일 내용
yaml_content = '''
format_version: 10
environment:
  seceret:
pipelines:
  pipeline-test_1:
    group: {codevuln_group}
    label_template: ${COUNT}
    lock_behavior: none
    display_order: -1
    materials:
      git-d86ad4c:
        git: {github_target_url}
        shallow_clone: false
        auto_update: true
        branch: main
    stages:
    - stage-test_1:
        fetch_materials: true
        keep_artifacts: false
        clean_workspace: false
        approval:
          type: success
          allow_only_on_success: false
        jobs:
          job-test_1:
            timeout: 0
            tasks:
              - exec:
                arguments:
                  - Upload test
                command: echo
                run_if: passed
'''

# GitHub API URL
url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

# 파일 내용을 base64로 인코딩
content_encoded = base64.b64encode(yaml_content.encode('utf-8')).decode('utf-8')

# GitHub API 요청 데이터
data = {
    "message": "Create or update CCIT_GoCD_PipelineCode.yaml",
    "content": content_encoded
}

# 요청 헤더
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 파일 생성 또는 수정 요청
response = requests.put(url, headers=headers, data=json.dumps(data))

# 응답 출력
if response.status_code in [200, 201]:
    print("File created or updated successfully.")
else:
    print(f"Error: {response.status_code} - {response.text}")
