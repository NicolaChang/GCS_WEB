# 20230829 網站滲透測試

## 網頁版檔案名稱及基本功能說明
### 資料夾名稱說明：
* static：圖片檔及JQ插入檔
* templates：HTML程式檔

### 檔案名稱說明：
* app.py：程式執行檔
* register.html：註冊頁面
* login.html：登入頁面
* privacy.html：隱私權聲明頁面
* Management.html：三大功能選擇頁面
* AccountManag.html：帳戶管理主頁面
* Account.html：帳戶無人機選擇頁面
* AccountInfo.html：機體資訊頁面
* AccountFlyHistory.html：飛行歷程頁面
* AccountRecord.html：飛行紀錄頁面-地圖
* Fleet.html：機隊管理頁面
* Drone.html：無人機管理主頁面
* addDrone.html：新增無人機頁面
* DroneMapVideo.html：單機視角和地圖頁面
* DronePlan.html：飛行計畫頁面
* DroneView.html：多重視角切換頁面
* DroneViews.html：四格視角及地圖頁面
* Mission.html：任務規劃主頁面
* MissionReview.html：建立任務名稱頁面
* MissionSet.html：任務規劃頁面
* logout.html：登出介面
* fullchain.pem：SSL憑證
* privkey.pem：SSL憑證
* requirements.txt：已安裝之套件清單

### 基本設定
* 虛擬環境名稱：GCSWEB
> `登入Putty->切換資料夾 cd Desktop/->切換虛擬環境 source GCSWEB/bin/activate ->進入檔案存放資料夾 cd env-wra/try-data/hjweb/GCSWeb/ ->輸入執行程式碼：python3 app.py，即可執行APP*`
* DNS：https://topologyuav.com:5002/Login/
