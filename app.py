
format_version: 10
pipelines:
  mongodb:
    group: gocd_test
    label_template: ${COUNT}
    lock_behavior: none
    display_order: -1
    materials:
      git:
        git: https://github.com/kigma00/mongo_gocdtest
        shallow_clone: false
        auto_update: true
        branch: main
    stages:
    - mongodb_stage:
        fetch_materials: true
        keep_artifacts: false
        clean_workspace: false
        approval:
          type: success
          allow_only_on_success: false
        jobs:
        - mongodb_job:
            timeout: 0
            tasks:
            - exec:
                command: /home/2024_CCIT_codevuln/Automation_Code/gocd-query-setting.sh
                argument:
                  - https://github.com/kigma00/mongo_gocdtest
                  - javascript
                run_if: passed
    