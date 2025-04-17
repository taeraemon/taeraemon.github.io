시계열을 다루는데 RNN을 쓰다가, 장기기억 관련 해결을 위해 LSTM을 다뤘었음.

이번에 다룰거는 Seq2Seq이랑 어텐션임

Seq2Seq는 입력 시퀀스를 받아서 다른 시퀀스로 변환하는 구조임. (ex 번역)

보통 인코더와 디코더를 쓰는데, LSTM으로 만들어져 있음.

그리고 긴 문장에서 중요한 정보를 집중하기 위한 어텐션까지 보고자 함. (Bahdanau, Luong)



---

### Seq2Seq

seq2seq는 인코더-디코터 모델이라고도 부름.

입력된 시퀀스를 다른 도메인의 시퀀스로 출력하는데 많이 쓰임 (ex 번역기)

<div style="text-align: center;">
  <img src="./01_seq2seq_simple.png" style="width:40%;"><br>
</div>

위와 같이 인코더가 입력 시퀀스를 고정된 길이의 context vector로 만듬.

그리고 디코더는 고정된 context vector을 받아서 시퀀스를 출력함.

내부의 셀을 다 쪼개보면 아래와 같이 동작함.


<div style="text-align: center;">
  <img src="./02_seq2seq_detail.png" style="width:80%;"><br>
</div>

인코더는 마지막 LSTM의 마지막 시점 은닉 상태를 전달. (context vector)

이거는 디코더의 첫 셀의 은닉 상태에 활용.

첫 셀의 데이터 입력은 sos로 시작.

첫 셀의 출력은 다음 셀의 입력에 진입. eos가 출력으로 나올 때까지 반복.


#### Teacher forcing

학습 단계에서는 Teacher forcing이라는게 활용됨.

학습 단계에서 직전 디코더의 출력이 입력으로 들어오다 보니, 첫 단추를 잘못 끼우면 연쇄적으로 학습이 안됨.

그래서 학습 단계에서는 각 셀의 입력에 정답을 넣어서 셀 별로 학습이 잘 되게 하는게 Teacher forcing.

근데 이러다 보니 테스트 과정에서 잘 안되기도 해서.. teacher forcing의 비율을 조절하는 scheduled sampling같은 이런저런 기법들이 제안됨.



&nbsp;
### Attention

seq2seq에 남아있던 문제를 해결하기 위한것 이었는데,
고정된 벡터에 압축하다보니 발생하는 정보 손실,
고질적인 기울기 소실

을 해결하고자 했음.


<div style="text-align: center;">
  <img src="./03_attention.png" style="width:80%;"><br>
</div>

그래서 기존 1차원 context vector만 넘기는게 아니라, 위와 같이 각 셀에서의 hidden state를 누적한 hs를 모두 활용.

그리고 이제 context vector을 디코더에 잘 넘겨야하는데 어떻게 할것이냐 !


<div style="text-align: center;">
  <img src="./04_attention_weight.png" style="width:80%;"><br>
</div>



디코더의 각 셀마다, $h_s$이 자신과 얼마나 중요한지를 감안한다. 이 역시 어떻게 하냐 !

현재 시점 디코더의 hidden state를 $h_t$라고 하자.

$ a_{attention\;weight} = h_s * h_t $ ->  내적을 통해 가중치를 계산

$ c_t = h_s * a $ -> 가중치와 context vector의 가중합 계산

다이어그램으로 풀어서 표현하면 아래와 같다.

<div style="text-align: center;">
  <img src="./05_attention_weightsum.png" style="width:80%;"><br>
</div>


결국, Attention이 적용된 Decoder의 계층은 아래와 같이 풀어서 그릴 수 있다.

<div style="text-align: center;">
  <img src="./06_attention_decoder.png" style="width:80%;"><br>
</div>



가중치 (어텐션 스코어)를 구하는 방식이 내적, 즉 dot-product 방식이었기 때문에 이는 dot-product attention이라 불린다.

이 외에도 scaled dot, general, concat, location-base등이 제안되었는데, dot, concat이 주로 다뤄지며 dot은 Luong, concat은 Bahdanau라고도 불린다.

다음은 트랜스포머를 다루게 된다.

---
