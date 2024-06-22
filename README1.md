# How to add service

Service란 번역을 위한 라이브러리 이름/ 모델 이름을 말한다.
서비스를 추가하기 위해선 다음 과정을 거치면 된다.

1. service.yaml에 **"서비스 이름":"호출할 클래스 이름"** 으로 API 호출만 하면 api_service에 모델을 불러오면 model_service에 추가한다.
   ![alt text](<image/Screenshot 2024-06-14 at 12.57.25.png>)

2. lingo_translate 폴더에서 추가한 서비스 방식에 추가한다.
   ![alt text](<image/Screenshot 2024-06-14 at 13.01.06.png>)

3. 해당 파일 안에 "호출할 클래스 이름"과 같은 클래스를 선언한다. 이때 Abstract 모델을 상속받아야 한다.
   ![alt text](<image/Screenshot 2024-06-14 at 13.02.44.png>)
