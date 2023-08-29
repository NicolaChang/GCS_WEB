<<<<<<< HEAD
# topology-back
# 簡介
Topology GCS 網站，該網站功能為讓使用者可以隨時觀看無人機上的直播影片、飛行資料等。
簡而言之，一個網頁版的Mission Planner的概念，當使用者註冊進入後。

使用者功能為
1. 無人機管理頁面新增無人機，新增後可以看到該無人機的機體資訊
2. 可至帳戶介面查看無人機的詳細機體資訊，如保險單、無人機型號等
3. 亦可建置任務，讓無人機執行(尚未撰寫)
4. 無人機連上網路後，可看到無人機的飛行資訊與直播畫面 

系統功能
1. 使用者密碼錯誤3次後，停用帳戶
2. 使用者註冊，帳號需有唯一性
3. 超過30分鐘未使用，將使用者登出 (未做)
4. 若帳號停用，會導向登入介面及顯示帳號停用 (未測試)
5. 登出後將使用者登入資料去除
6. 分割飛行歷程、任務飛行紀錄表 (未定案)
7. 自動記錄飛行資料
8. 飛行歷程的里程計算、總時長 (未定案)
9. 傳輸 RTMP流的 URL 給前端 (未做)
10. 自動錄RTMP串流直播的影片 (未測試)
11. 無人機里程計算(未測試)
12. 新增無人機，無人機流水號有唯一性
13. 新增無人機，同使用者無人機名稱不能相同
14. 前端將任務規劃，傳至後端 (未做)
15. 將任務存成檔案放在後端 (未做)
16. 任務傳輸至無人機上 (未做)

# 程式說明
## 如何開啟網站

先至程式存放路徑 `cd /home/hj-back/Desktop/env-wra/try-data/hjweb/FFront`

使用虛擬環境(目前有rtc、back-web、webdj) `workon rtc`

輸入 `python3 app.py`

即可至 `59.120.184.126:5001/Login/` 做網頁測試

## 使用的函式庫與版本
Flask為web server的基底，然後抓取資料存進mysql server中
```
Flask==2.2.3
Flask_SocketIO==5.3.3
opencv_python==4.7.0.72
paho_mqtt==1.6.1
PyMySQL==1.0.3
Werkzeug==2.2.3
```


## 網頁資料各參數
參數文件的[json檔](https://drive.google.com/file/d/1rEqFnbA-WWDfeJhp1j9xLf_-AYZB85ok/view?usp=share_link)

可參考[此檔案](https://docs.google.com/presentation/d/1SUw9Zk8-8PQJUEiGDZvI6HTvSqwyC5VbsB8AgaBF7c0/edit#slide=id.g24f2fef54e4_0_18)
就能用視覺化的方式看各參數
=======
# GCS_WEB
>>>>>>> 612be7ed388f4ea976b7a7fe858f8b55c1381b7f
