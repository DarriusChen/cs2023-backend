# 安裝說明
## 開發環境
請在``vscode``下開發，利用``pdm init``和``pdm install``完成虛擬環境建置

## 安裝包
這是一個devlop的模板樣式，已經安裝了下列package
* pylint
* black
* commitizen
* pre-commit
* pytest
* allure
```diff
- 請記得利用 cz init 初始化
! 請記得利用 pre-commit 導入自定義規則
```
# 注意事項
### 請更改``github/workflows的ci.yml``
```yaml=
      - name: Teams-connection
        uses: ./ms-teams-deploy-card-master
        if: always()
        with:
          github-token: ${{ github.token }}
          webhook-uri: ${{ secrets.MS_TEAMS_WEBHOOK_URI }}
          card-layout-exit: complete
          environment: ${{ github.ref }}
          timezone: Asia/Taipei
          show-on-start: false
          custom-actions: |
            - text: View PR
              url: "請自己設定超連結"
            - text: View CI
              url: "請自己設定超連結"
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```
### 請記得設定``MS_TEAMS_WEBHOOK_URI``＆``ALLURE``的TOKEN