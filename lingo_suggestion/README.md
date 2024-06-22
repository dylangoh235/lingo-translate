모델을 로드하는 .py 파일과 synonym을 추천하는 suggestion 메소드를 포함하는 class 명을 기록해야 합니다.
class는 target_word를 반드시 인자로 받아야합니다. 맥락 처리 프로세스가 있다면 text, cntxt_len 또한 인자로 받습니다.
model_load.py의 Abstract class를 상속받아서 해결할 수도 있습니다.

모델의 weight, checkpoint는 /lingo_suggestion/models/checkpoints/ 에 로드합니다.
모델 실행 .py는 /lingo_suggestion/models/ 에 업로드합니다.

service.yaml에 .py 파일명과 class 명을 기록해야합니다.

