
import requests
import base64
import json
import urllib3

http = urllib3.PoolManager()

def send_slack_message():
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not slack_webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")


    # 메시지 내용 설정
    message_content = "GoCD 파이프라인 생성"

    # 슬랙 메시지 생성
    slack_message = {
        "text": message_content
    }

    # 슬랙으로 메시지 전송
    try:
        encoded_message = json.dumps(slack_message).encode('utf-8')
        response = http.request('POST', slack_webhook_url, body=encoded_message, headers={'Content-Type': 'application/json'})
        print(f"Response status: {response.status}")
        print(f"Response data: {response.data.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending message to Slack: {e}")
        return {
            'statusCode': 500,
            'body': f"Error sending message to Slack: {e}"
        }

    return {
        'statusCode': response.status,
        'body': response.data.decode('utf-8')
    }

def update_github_config():
    # GoCD 설정 입력받기
    GoCD_pipeline = "mongodb"  # GoCD 파이프라인 이름
    GoCD_giturl = "https://github.com/kigma00/mongo_gocdtest"  # Git 저장소 URL
    test_shell_script = "/home/2024_CCIT_codevuln/Automation_Code/gocd-query-setting.sh"  # 파이프라인에서 실행할 셸 스크립트
    GoCD_group = "gocd_test"  # GoCD 그룹 이름

    # GitHub 저장소 업데이트 설정 입력받기
    Github_owner = "kigma00"  # GitHub 소유자 (사용자명 또는 조직명)
    Github_repo = "CCIT_GoCD_PipelineCode"  # GitHub 저장소 이름
    Github_token = os.getenv("GITHUB_TOKEN")  # GitHub 개인 액세스 토큰
     if not Github_token:
        raise ValueError("GITHUB_TOKEN 환경 변수가 설정되지 않았습니다.")
    
    
    Github_path = f"{GoCD_pipeline}.gocd.yaml"  # GitHub 저장소에 저장할 YAML 파일 경로

    # YAML 파일 생성
    template = f'''
    format_version: 10
    pipelines:
      {GoCD_pipeline}:
        group: {GoCD_group}
        label_template: ${COUNT}
        lock_behavior: none
        display_order: -1
        materials:
          git:
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
                    argument:
                        - https://github.com/kigma00/mongo_gocdtest
                        - javascript
                    run_if: passed
    '''

    # GitHub API에 업데이트 요청
    url = f'https://api.github.com/repos/{Github_owner}/{Github_repo}/contents/temp/{Github_path}'

    # 요청 헤더 설정
    headers = {
        'Authorization': f'token {Github_token}',  # 인증 토큰
        'Content-Type': 'application/yaml',  # 콘텐츠 유형
        'Accept': 'application/vnd.github.v3+json'  # GitHub API 버전
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
        "message": f"Update {Github_path}",  # 커밋 메시지
        'content': content_encoded  # 인코딩된 파일 내용
    }

    if sha:
        data['sha'] = sha  # 기존 파일의 SHA 값 추가

    # 파일 생성 또는 수정 요청
    response = requests.put(url, headers=headers, json=data)

    # 응답 출력
    if response.status_code in [200, 201]:
        print("File created or updated successfully.")  # 파일 생성 또는 업데이트 성공
    else:
        print(f"Error: {response.status_code} - {response.text}")  # 오류 발생 시 메시지 출력

if __name__ == "__main__":
    update_github_config()  # GitHub 설정 업데이트
    result = send_slack_message()  # Slack 메시지 전송
    print(result)
    