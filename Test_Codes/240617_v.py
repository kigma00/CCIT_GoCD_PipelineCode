import requests
import json
import base64

# 사용자 입력 받기 및 검증
def get_input(prompt):
    value = input(prompt)
    while not value.strip():
        print("이 필드는 필수 입력 사항입니다.")
        value = input(prompt)
    return value

owner = get_input("GitHub 사용자 이름: ")
repo = get_input("GitHub 리포지토리 이름: ")
path = get_input("파일 경로 (예: CCIT_GoCD_PipelineCode.yaml): ")
token = get_input("GitHub Personal Access Token: ")
codevuln_group = get_input("파이프라인 그룹 이름: ")
github_target_url = get_input("Git 저장소 URL: ")

# GitHub API URL
url_get = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

# 요청 헤더
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 파일 상태 조회 및 SHA 값 추출
try:
    response_get = requests.get(url_get, headers=headers)
    response_get.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
    if response_get.status_code == 200:
        sha = response_get.json()['sha']
    else:
        sha = None
except requests.exceptions.RequestException as e:
    print(f"파일 상태 조회 중 오류 발생: {e}")
    sha = None

# YAML 파일 내용
yaml_content = f'''
format_version: 10
pipelines:
  pipeline-test_1:
    group: {codevuln_group}
    label_template: ${{COUNT}}
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
    "message": f"Update {path}",
    "content": content_encoded,
}

if sha:
    data["sha"] = sha  # SHA 값 추가

# 파일 생성 또는 수정을 위한 URL
url_put = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

# 파일 생성 또는 수정 요청
try:
    response_put = requests.put(url_put, headers=headers, data=json.dumps(data))
    response_put.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
    if response_put.status_code in [200, 201]:
        print("파일이 성공적으로 생성되거나 업데이트되었습니다.")
    else:
        print(f"오류: {response_put.status_code} - {response_put.text}")
except requests.exceptions.RequestException as e:
    print(f"파일 생성 또는 수정 중 오류 발생: {e}")
