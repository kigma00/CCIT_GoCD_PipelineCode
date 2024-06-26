
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
    