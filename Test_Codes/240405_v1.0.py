import requests
import base64

# GoCD_Setting
GoCD_pipeline = input("GoCD_pipeline_name :")
GoCD_giturl = input("git_url :")
test_shell_script = input("executeshell_script :")
GoCD_group = input("Group_name :")

#Github_repo_update_Setting
Github_owner = input("Github_owner :")
Github_repo = input("Github_repository_name :")
Github_token = input("token :")
Github_path = {GoCD_pipeline}.yaml

# Create YAML file 
template = 
f'''
format_version: 10
pipelines:
  {GoCD_pipeline}:
    group: {GoCD_group}
    label_template: ${{COUNT}}
    lock_behavior: none
    display_order: -1
    materials:
      git-fdee270:
        git: {GoCD_giturl}
        shallow_clone: false
        auto_update: true
        branch: main
    stages:
    - {GoCD_pipeline}_stage:
        fetch_materials: true
        keep_artifacts: false
        clean_workspace: false
        approval:
          type: success
          allow_only_on_success: false
        jobs:
          {GoCD_pipeline}_job:
            timeout: 0
            tasks:
            - exec:
                command: {test_shell_script}
                run_if: passed
    '''
    
# GitHub API에 업데이트 요청
url = f'https://api.github.com/repos/{Github_owner}/{Github_repo}/contents/temp/{Github_path}'

# 요청 헤더
headers = {
    'Authorization': f'token {Github_token}',
    'Content-Type': 'application/yaml',
    'Accept': 'application/vnd.github.v3+json'
}

# 파일 상태 조회
response_get = requests.get(url, headers=headers)

# 파일이 존재하는 경우 SHA 값을 추출
if response_get.status_code == 200:
    sha = response_get.json()['sha']
else:
    sha = None  
    
# 파일 내용을 base64로 인코딩
content_encoded = base64.b64encode(template.encode('utf-8')).decode('utf-8')

# GitHub API 요청 데이터 (SHA 값을 포함하여 업데이트하는 경우)
data = {
    "message": "Update {Github_path}",
    'content': base64.b64encode(template.encode()).decode()
}

# 파일 생성 또는 수정 요청
response = requests.put(url, headers=headers, json=data)

# 응답 출력
if response.status_code in [200, 201]:
    print("File created or updated successfully.")
else:
    print(f"Error: {response.status_code} - {response.text}")    
