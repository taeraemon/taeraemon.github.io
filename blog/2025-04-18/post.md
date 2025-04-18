# Transformer

Transformer는 2017년 발표된 논문 **“Attention Is All You Need”** 를 기반으로 한 모델이다.  
기존 Seq2Seq 구조(인코더–디코더)를 유지하면서도, RNN 없이 **오직 어텐션만**으로 동작하는 것이 특징이다.

---

## 1. 기존 Seq2Seq의 한계

기존 Seq2Seq 모델은 인코더가 문장 전체를 **Context Vector 하나로 압축**해 디코더에 넘기기 때문에,  
문장이 길어질수록 정보 손실이 발생한다.

이를 보완하기 위해 어텐션이 도입되었고,  
Transformer는 이를 확장하여 **어텐션만으로 인코더-디코더 전체를 구성**한다.

---

## 2. 트랜스포머의 하이퍼파라미터

- $d_{model} = 512$ : 임베딩 벡터의 차원 (인코더-디코더 공통)
- $\texttt{num_layers} = 6$ : 인코더 및 디코더의 층 수
- $\texttt{num_heads} = 8$ : 병렬 어텐션 헤드 수
- $d_{ff} = 2048$ : FFNN의 히든 레이어 차원 수

---

## 3. 트랜스포머 전체 구조

<div style="text-align: center;">
  <img src="./01.png" style="width:30%;"><br>
  <span>Transformer의 기본 구조</span>
</div>

Transformer는 시점(time-step)마다 나뉜 RNN 구조와 달리,  
인코더와 디코더 각각이 여러 층(layer)으로 구성된 병렬 구조를 가진다.

---

## 4. Positional Encoding

RNN은 순차적으로 입력을 받기 때문에 순서 정보가 자연스럽게 포함되지만,  
Transformer는 **입력을 병렬로 처리하므로 위치 정보를 명시적으로 추가**해야 한다.

<div style="text-align: center;">
  <img src="./02.png" style="width:60%;"><br>
  <span>위치 정보 인코딩 방식</span>
</div>

### 4.1 인코딩 공식

<div style="text-align: center;">
$PE_{(pos, 2i)} = \sin \left( \frac{pos}{10000^{2i / d_{model}}} \right)$,  
$PE_{(pos, 2i+1)} = \cos \left( \frac{pos}{10000^{2i / d_{model}}} \right)$
</div>

사인/코사인은 주기 함수이므로, **상대적인 위치 정보를 자연스럽게 표현**할 수 있다.

<div style="text-align: center;">
  <img src="./03.png" style="width:40%;"><br>
</div>

<div style="text-align: center;">
  <img src="./04.png" style="width:40%;"><br>
  <span>예시: 50단어 × 128차원</span>
</div>

---

## 5. Attention

Transformer에는 총 3가지 어텐션 메커니즘이 존재한다.

<div style="text-align: center;">
  <img src="./05.png" style="width:30%;"><br>
</div>

- **Self-Attention** : Query, Key, Value가 모두 같은 소스 (인코더 또는 디코더 내부)
- **Encoder-Decoder Attention** : Query는 디코더에서, Key/Value는 인코더에서 생성

<div style="text-align: center;">
  <img src="./06.png" style="width:50%;"><br>
  <span>어텐션 종류별 흐름</span>
</div>

---

## 6. Self-Attention의 구조

### 6.1 Q, K, V의 정의

- 기존 Seq2Seq:
  - Query: 디코더의 특정 시점 출력
  - Key/Value: 인코더의 전체 은닉 상태

- Transformer:
  - Query, Key, Value 모두: **입력 문장의 각 단어 벡터**

<div style="text-align: center;">
  <img src="./07.png" style="width:40%;"><br>
</div>

---

### 6.2 Q, K, V 만들기

<div style="text-align: center;">
  <img src="./08.png" style="width:30%;"><br>
</div>

입력 임베딩에 선형 변환을 적용하여 Q, K, V를 생성한다.

---

### 6.3 Scaled Dot-Product Attention

- Q와 K의 내적 → **Attention Score**
- Score에 softmax → **Attention Weight (확률 분포)**
- Weight와 V의 가중합 → **Attention Output**

<div style="text-align: center;">
  <img src="./09.png" style="width:30%;"><br>
</div>

<div style="text-align: center;">
  <img src="./10.png" style="width:30%;"><br>
</div>

**Scaling ($\sqrt{d_k}$)** 은 차원이 클수록 score가 커지는 문제를 방지하여  
softmax의 gradient 소실을 막는다.

<div style="text-align: center;">
$Attention(Q, K, V) = \text{softmax}\left( \frac{QK^T}{\sqrt{d_k}} \right) V$
</div>

---

### 6.4 Multi-Head Attention

- 여러 개의 Head에서 Q, K, V를 각각 다른 파라미터로 projection하여 Attention 수행
- 결과를 concat 후, 선형 변환 $W^O$를 통해 $d_{model}$ 차원으로 맞춤

<div style="text-align: center;">
  <img src="./14.png" style="width:40%;"><br>
</div>

<div style="text-align: center;">
  <img src="./15.png" style="width:20%;"><br>
</div>

<div style="text-align: center;">
  <img src="./16.png" style="width:30%;"><br>
  <span>최종 출력: $(\texttt{seq_len}, d_{model})$</span>
</div>

---

## 7. Position-wise Feed Forward Neural Network (FFNN)

Attention은 선형 조합만 처리할 수 있으므로, 비선형 표현 학습을 위해  
각 위치마다 같은 구조의 FFNN을 독립적으로 적용한다.

<div style="text-align: center;">
  <img src="./17.png" style="width:60%;"><br>
</div>

<div style="text-align: center;">
  <img src="./18.png" style="width:20%;"><br>
  <span>$FFNN(x) = \max(0, xW_1 + b_1) W_2 + b_2$</span>
</div>

---

## 8. 디코더 구조

### 8.1 Look-Ahead Mask

디코더는 미래 단어를 보면 안 되기 때문에,  
**학습 시에도 뒤 단어를 마스킹하여 순차적으로 학습**하게 한다.

<div style="text-align: center;">
  <img src="./19.png" style="width:30%;"><br>
</div>

<div style="text-align: center;">
  <img src="./20.png" style="width:20%;"><br>
</div>

즉, 디코더가 미래 단어를 보지 못하게 하여  
**앞 단어만 보고 다음 단어를 예측**하게 만드는 것이 핵심이다.

---

### 8.2 Encoder-Decoder Attention

디코더의 두 번째 서브층에서는  
지금까지 생성한 단어들을 바탕으로 인코더 출력을 참조한다.

- Query: 디코더의 출력
- Key/Value: 인코더의 출력

---

## 9. Residual Connection & Layer Normalization

Transformer의 모든 서브층(Self-Attention, FFNN 등)은 다음과 같은 구조를 따른다:

<div style="text-align: center;">
$ \text{LayerNorm}(x + \text{Sublayer}(x)) $
</div>

이 구조는 **Gradient 흐름을 안정화**시키고, **학습 수렴 속도를 높인다.**

---

## 🔗 Reference

- https://arxiv.org/abs/1706.03762  
- https://wikidocs.net/31379
