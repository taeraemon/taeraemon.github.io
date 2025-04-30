# Vision Transformer (ViT)

---

## 목차
1. 개요
2. Vision Transformer (ViT)
   - 전체 구조
   - 주요 컴포넌트
   - 학습 방법

3. ViT Variations
   - DeiT (Data-efficient Image Transformers)
   - Swin Transformer (Shifted Window Transformer)
   - DETR (DEtection TRansformer)
   - MAE (Masked Autoencoder)

4. 비전 태스크별 적용
   - Classification
   - Object Detection
   - Segmentation

5. 최신 연구 동향
   - Foundation Models (CLIP, DALL-E, Florence)
   - Multimodal Transformers
   - Efficient Transformers (MobileViT, EfficientViT)

---

## 1. 개요

텍스트 처리에서 Transformer는 긴 문맥 이해, 병렬 처리에서 GOAT 성능 달성.

이를 비전에도 적용하고자 하여, CNN이 고정된 크기의 커널로 인해 long-range dependency에 대한 한계에 주목.

이미지 한 장을 여러 패치로 쪼개서, 단어 토큰 다루듯이 처리하는 방식으로 Transformer을 적용하여 기존 한계 극복.

(CNN은 입력위치가 변하면 출력 위치도 변할거라는 Translation equivariance 가정과, 이미지의 일부만 봐도 특징을 추출할 수 있다는 Locality 가정을 해서 그냥 MLP보다 성능이 좋았음. 킹치만 Transformer는 이 두개로부터 자유로워서 표현은 더욱 자유로우나, 대신 데이터셋이 충분하지 못하면 성능이 오히려 더욱 떨어짐 )

---

## 2. Vision Transformer (ViT)
- 전체 구조 개요
- Patch Embedding
- Class Token
- Position Embedding
- Transformer Encoder
- MLP Head
- 학습 방법

---

## 3. ViT Variations
### 3.1 DeiT (Data-efficient Image Transformers)
- 등장 배경
- 주요 특징
- Knowledge Distillation
- 성능 비교

### 3.2 Swin Transformer
- 계층적 구조
- Shifted Window
- 계산 효율성
- 확장성

### 3.3 DETR (Detection Transformer)
- Object Detection에의 적용
- Bipartite Matching
- Transformer Decoder
- 성능 분석

### 3.4 MAE (Masked Autoencoder)
- Self-supervised Learning
- Masking 전략
- Reconstruction
- 성능 평가

---

## 4. 비전 태스크별 적용
### 4.1 Classification
- ImageNet 성능
- Fine-tuning 전략
- 실용적 팁

### 4.2 Object Detection
- DETR 구조
- End-to-end Detection
- 성능 비교

### 4.3 Segmentation
- ViT 기반 Segmentation
- Mask Transformer
- 성능 분석

---

## 5. 최신 연구 동향
### 5.1 Foundation Models
- CLIP
- DALL-E
- Florence

### 5.2 Multimodal Transformers
- Vision-Language Models
- Cross-modal Attention
- 응용 사례

### 5.3 Efficient Transformers
- MobileViT
- EfficientViT
- 경량화 전략


---


## 🔗 Reference
- https://velog.io/@leehyuna/Vision-TransformerViT


