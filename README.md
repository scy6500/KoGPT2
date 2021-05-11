# KoGPT2

This project generate korean using KoGPT2 model.

Github: [SKT-AI KoGPT2](https://github.com/SKT-AI/KoGPT2)

License : [CC-BY-NC-SA 4.0](https://github.com/SKT-AI/KoGPT2/blob/master/LICENSE)

### Post parameter

    text: Korean
    length: The length of text


### Output format

    {"0": generated text}


## * With CLI *

### Input example


    curl -X POST "https://main-ko-gpt2-scy6500.endpoint.ainize.ai" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text= 비트코인은 오를까요?"
    

### Output example


    {
      "0": "비트코인은 오를까요?" "좋다, 좋아. 나는 지금 비트코인을 가지고 있지. 당신이 비트코인이면 돈의 일부라도 내줄 수 있다."
    }


## * With swagger *

API page: [Ainize](https://ainize.ai/scy6500/KoGPT2?branch=main)

## * With a Demo *

Demo page: [End-point](https://main-ko-gpt2-scy6500.endpoint.ainize.ai)
