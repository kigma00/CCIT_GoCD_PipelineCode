#!/bin/bash

# 기본 설정
owner="kigma00"  # GitHub 사용자 이름
repo="CCIT_GoCD_PipelineCode"  # GitHub 리포지토리 이름
path="CCIT_GoCD_PipelineCode.yaml"  # 생성하거나 수정할 파일의 경로
token="{token}"  # GitHub Personal Access Token
api_url="https://api.github.com/repos/$owner/$repo/contents/$path"

# 파일의 현재 상태를 조회하여 SHA 값을 얻습니다.
sha=$(curl -s -H "Authorization: token $token" $api_url | jq -r '.sha')

# YAML 파일 내용
yaml_content=$(cat <<EOF
format_version: 10
environment:
  secret:
pipelines:
  pipeline-test_1:
    group: {codevuln_group}
    label_template: \${COUNT}
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
EOF
)

# 파일 내용을 base64로 인코딩
content_encoded=$(echo -n "$yaml_content" | base64)

# 파일 생성 또는 수정 요청 데이터 준비
data="{\"message\": \"Update $path\", \"content\": \"$content_encoded\""
if [[ -n "$sha" ]]; then
    data="$data, \"sha\": \"$sha\""
fi
data="$data}"

# 파일 생성 또는 수정 요청
response=$(curl -s -X PUT -H "Authorization: token $token" -H "Content-Type: application/json" -d "$data" $api_url)

# 응답 출력
echo $response | jq .
