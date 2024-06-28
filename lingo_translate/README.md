# 서비스 추가하는 법

### 1. `service.yaml` 파일 수정

먼저 서비스를 추가하려면 해당 서비스가 API만 호출하는지 아닌지를 확인해야합니다.
만약 API만 호출한다면 api_services, 아니라면 model_services 입니다.
서비스를 추가하려면 `service.yaml` 파일에 다음과 같은 형식으로 작성합니다.

예를 들어, "torch_transformer"이라는 서비스를 추가하고, 이를 호출하기 위해 "TorchTransformerModel"라는 클래스를 사용한다고 가정하면 다음과 같이 작성합니다.

```yaml
model_services:
  torch_transformer: TorchTransformerModel
```

### 2. 서비스 형태에 맞게 모듈 추가

이제 `lingo_translate` 폴더에서 추가한 서비스 방식에 맞게 코드를 작성합니다. 예를 들어, `TorchTransformerModel`를 추가하기 위해 `model_modules` 폴더 안에 새로 추가할 서비스 파일 `torch_transformer_module` 을 추가합니다:

```plaintext
lingo_translate/
    api_modules/
        ...
    model_modules/
        torch_transformer_module.py
```

### 3. "호출할 클래스 이름" 정의

다음 `lingo_translate/model_modules/torch_transformer_module.py` 파일에서 `TorchTransformerModel` 클래스를 정의합니다. 이 클래스는 `AbstractModel` 모델을 상속받아야 합니다.

```python
# torch_transformer_module.py

from lingo_translate.mapper import AbstractModel

class TorchTransformerModel(AbstractModel):
    ...
    def translate(self, text, source_lang, target_lang):
        # 번역 로직
        pass
```

위의 예시에서는 `TorchTransformerModel` 클래스가 `AbstractModel` 클래스를 상속받고 있으며, 번역 로직을 처리하는 `translate` 메서드를 정의하고 있습니다.

추가할 때마다 `service.yaml` 파일과 `lingo_translate` 폴더에 새 클래스를 정의하는 파일을 생성해야 합니다.
