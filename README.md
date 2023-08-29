# 20230829 

## 網站滲透測試檔案說明
### 資料夾名稱說明：
* static：圖片檔及JQ插入檔
* templates：HTML程式檔

### 檔案名稱及基本功能說明：
* app.py：程式執行檔
* register.html：註冊頁面 `兩次密碼輸入不同會鎖確認按鈕，註冊帳號重複會顯示提醒視窗`
* login.html：登入頁面 `按忘記密碼顯示對話框，登入成功會跳至下一頁，失敗回再登入介面`
* privacy.html：隱私權聲明頁面 `登入介面會自動讀取mysql資料，每個帳號只會顯示一次`
* Management.html：三大功能選擇頁面
* AccountManag.html：帳戶管理主頁面
* Account.html：帳戶無人機選擇頁面
* AccountInfo.html：機體資訊頁面
* AccountFlyHistory.html：飛行歷程頁面
* AccountRecord.html：飛行紀錄頁面-地圖
* Fleet.html：機隊管理頁面
* Drone.html：無人機管理主頁面 `點擊指定無人機會傳無人機名稱及流水號至即時資訊頁面`
* addDrone.html：新增無人機頁面 `新增無人機自動將資料存至mysql`
* DroneMapVideo.html：即時資訊頁面 `讀取即時FlightData顯示在頁面上，並根據即時經緯度繪製地圖軌跡，即時影像為RTSP串流影像`
* DronePlan.html：飛行計畫頁面 `點選任務名稱一次只能選一項任務`
* DroneView.html：多重視角切換頁面 `多重視角表格顯示前四台無人機名稱，並將無人機名稱傳至下一頁`
* DroneViews.html：四格視角及地圖頁面 `讀取前四台無人機名稱，即時資料尚未規劃，四格RTSP影像目前為相同`
* Mission.html：任務規劃主頁面
* MissionReview.html：建立任務名稱頁面
* MissionSet.html：任務規劃頁面
* logout.html：登出介面 `選擇確認跳至登入介面，選擇返回介面跳至三大功能選擇頁面`
* fullchain.pem：SSL憑證
* privkey.pem：SSL憑證
* requirements.txt：已安裝之套件清單

### 基本設定
* 虛擬環境名稱 GCSWEB：
  * `登入Putty->切換資料夾 cd Desktop/->切換虛擬環境 source GCSWEB/bin/activate ->進入檔案存放資料夾 cd env-wra/try-data/hjweb/GCSWeb/ ->輸入執行程式碼：python3 app.py，即可執行APP`
* DNS：https://topologyuav.com:5002/Login/
* 測試帳號密碼：
  * `帳號：test00@gmail.com (已內建一台無人機可做數據顯示測試)、密碼：Zxc123123`
* RTSP串流影像指令：
  * ‵raspivid -t 0 -w 1280 -h 720 -fps 15 -g 75 -fl -o - | ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i pipe:0 -c:v copy -c:a aac -strict experimental -f rtsp -rtsp_transport tcp rtsp://59.120.184.126:8554/mystream`
