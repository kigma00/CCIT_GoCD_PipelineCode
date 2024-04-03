import requests
import json
import base64

# 기본 설정
owner = 'kigma00'  # GitHub 사용자 이름
repo = 'CCIT_GoCD_PipelineCode'  # GitHub 리포지토리 이름
path = 'CCIT_GoCD_PipelineCode.yaml'  # 생성하거나 수정할 파일의 경로
token = '{token}'  # GitHub Personal Access Token

# 파일의 현재 상태를 조회하여 SHA 값을 얻기 위한 URL
url_get = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

# 요청 헤더
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 파일 상태 조회
response_get = requests.get(url_get, headers=headers)

# 파일이 존재하는 경우 SHA 값을 추출
if response_get.status_code == 200:
    sha = response_get.json()['sha']
else:
    sha = None

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

# 파일 내용을 base64로 인코딩
content_encoded = base64.b64encode(yaml_content.encode('utf-8')).decode('utf-8')

# GitHub API 요청 데이터 (SHA 값을 포함하여 업데이트하는 경우)
data = {
    "message": "Update {path}",
    "content": content_encoded,
    "sha": sha  # SHA 값 추가
}

# 파일 생성 또는 수정을 위한 URL
url_put = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

# 파일 생성 또는 수정 요청
response_put = requests.put(url_put, headers=headers, data=json.dumps(data))

# 응답 출력
if response_put.status_code in [200, 201]:
    print("File created or updated successfully.")
else:
    print(f"Error: {response_put.status_code} - {response_put.text}")
