# TODO



시스템 모델링 - 선형시스템, 상태공간, 전달함수, 시스템 응답, 안정성(Lyapunov, Routh-Hurwitz, Nyquist), 제어가능성, 관측가능성

동역학 모델링 - Sloshing, TWD, Flexible Body Dynamics, Multi-body Dynamics, Fuel Slosh, Inverted Pendulum

추정 - KF, EKF, UKF, PF, GP

항법 - INS, GPS, INS/GPS LC TC, INS/UWB, INS/Radar Alti, federated, Radar

유도 - PNG, PEG, Convex Optimization, Optimal Control, Lambert Guidance, Q-Law

제어 - PID, LQR, MPC

신호처리 - FFT, STFT, Wavelet, Radar Signal Processing, Beamforming, SDR

강화학습 - DQN, PPO, SAC

SLAM - Visual, LiDAR, VIO, LIO-SAM

Path Planning - A*, RRT, PRM, D*, Hybrid A*

궤도역학 - Two-body Problem, Perturbations, Orbital Elements, Coordinate Systems, Orbit Determination, Orbit Propagation, Lambert's Problem, Hohmann Transfer, Bi-elliptic Transfer, Low-thrust Trajectory



비전 - 탐지
    - Two-stage Detector
        R-CNN (2014): Selective Search + CNN → SVM, 최초의 CNN 기반 detector
        Fast R-CNN (2015): 전체 이미지를 한 번에 CNN에 통과, RoI Pooling 도입
        Faster R-CNN (2015): RPN(Region Proposal Network) 도입으로 end-to-end 구조 완성
        Mask R-CNN (2017): Faster R-CNN에 segmentation branch 추가
        Cascade R-CNN (2018): IoU 기준을 점차 높이며 학습, 정확도 향상
        Sparse R-CNN (2021): anchor 없이 query 기반으로 object detection 수행

    - One-stage Detector (Anchor-based)
        YOLOv1 (2016): Grid 기반으로 한 번에 클래스 + 박스 예측
        SSD (2016): 다양한 크기의 feature map에서 anchor box 예측
        YOLOv2~v3 (2017~2018): anchor box 도입, multi-scale 대응
        RetinaNet (2017): Focal Loss 도입으로 class imbalance 문제 해결

    - One-stage Detector (Anchor-free)
        CornerNet (2018): top-left, bottom-right keypoint 예측
        CenterNet (2019): 객체 중심점 heatmap 예측 + 크기 복원
        FCOS (2019): 각 위치에서 직접 bounding box 예측
        DETR (2020): Transformer 기반 object query 방식
        YOLOX (2021): YOLO 구조 기반 + anchor-free + SimOTA 학습 방식

비전 - 분할
    - Semantic Segmentation
        FCN (2015): CNN을 fully conv로 대체, 최초의 세그멘테이션 네트워크
        U-Net (2015): 의료 이미지에서 활약, skip connection 구조
        DeepLab v3+ (2018): Atrous conv, encoder-decoder 형태

    - Instance Segmentation
        Mask R-CNN (2017): Faster R-CNN에 마스크 브랜치 추가

    - Panoptic Segmentation
        Panoptic FPN (2019): FPN 기반, semantic+instance 결합
        UPSNet (2019): 두 segmentation 결과를 자연스럽게 합침

    - Foundation 모델
        SAM (2023): Segment Anything Model, zero-shot으로 모든 걸 잘라냄

비전 - 생성
    - Autoencoder 계열
        Autoencoder (AE): 인코더-디코더 구조로 입력 복원
        VAE (2013): 잠재 공간을 확률 분포로 모델링해 샘플링 가능
        CVAE: 클래스 조건 등을 입력으로 추가해 조건부 생성 가능

    - GAN 계열
        GAN (2014): 생성자(Generator)와 판별자(Discriminator)의 경쟁 구조
        DCGAN (2015): CNN을 이용해 GAN을 이미지 생성에 적합하게 구성
        CycleGAN (2017): 비지도 이미지-이미지 변환 (horse ↔ zebra 등)
        StarGAN (2018): 하나의 네트워크로 다중 도메인 이미지 변환
        PGGAN (2017): 낮은 해상도 → 높은 해상도로 점진적 학습 (ProGAN)
        StyleGAN (2018~2021): 스타일 벡터로 이미지 조절 가능 (StyleGAN2, 3 발전됨)

    - Diffusion 계열
        DDPM (2020): Denoising Diffusion Probabilistic Model, 노이즈 제거 기반 생성

비전 - Tracking

비전 - 3D Vision / Depth Estimation

비전 - Pose Estimation

