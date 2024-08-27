# Audio_waterMark_simulator
음성 통신간 피싱 공격 방지를 위한 Realtime Audio Digital Signature Simulator.

# OutLine
### Background
기관 사칭형 보이스피싱 범죄는 2016년 3,384건에서 2023년 11,314건으로 3배 이상 증가, Generative AI 기술이 급속히 발전함에 따라 Deep voice 기술을 활용한 보이스피싱 범죄 사례 및 피해 규모도 증가하는 추세이다. 
### Solution(Main Idea)
인가된 기관이 발신하는 전화에 digital signature를 추가하여 송신, 이를 수신자가 추출 및 검증하여 인가된 기관임을 확인한다. 인가된 기관으로부터 발신된 전화임을 인증하는 기술은 역으로 비 인가된 기관으로부터 발신된 전화임을 증명할 수 있으므로, 기관 사칭형 보이스피싱 범죄에 효율적인 대응 방안이 될 것이다.
### Program
해당 프로그램은 실시간 통신 환경을 묘사하여 이러한 Digital signaure의 삽입과 추출, 검증 및 판별 과정을 구현한 것이다.

## Excution screen
![화면 캡처 2024-07-23 162352](https://github.com/user-attachments/assets/aee2c5e3-192d-4462-b693-5cea9c81c09b)

## Menu
### Sound file
import or record an audio file (Audio file은 1 Channel 16,000Hz (.wav) 음성 파일)

### Watermark
For the insertion/extraction test of digital signature.
[Create And insert] : Insert digital signature into the selected audio file 

[Extract] : Extract digital signature from the selected audio file

### Realtime Simulation
 Realtime 음성 통신 환경에서의 Simulation
 - (setting) : Simulation의 mode 설정 기능, Caller가 인가된 금융 기관인지, 금융 기관을 사칭한 공격 단체인지 설정 가능

 - (Excution) : 위 설정으로 Simulation 실행
    - [Make a call] : 전화 통신 Simulation 시작
    - [hang up] : 전화 통신 Simulation 종료

Watermark 검출 및 미검출로 인한 인가된 금융 기관 판단 여부에 걸린 시간(Detect Time)과 판단 결과(Detect Result)를 표시

## Algorithm
### Create digital signature bitstream 
Data는 2,048bit의 Binary Data로 이루어져 있으며, 출처 데이터와 time stamp, CRC Code로 구성된다.
### Insert digital signature bitstream 
Spread-spectrum 기법을 사용하여 삽입하였다. 
digital signature 2,048bit Binary Data는 음성으로 1초의 분량으로 표현되며, 삽입은 통화 초기에 N번 삽입되는데, 원활한 추출을 위해 여백 0.1초를 포함한 1.1초를 주기로 삽입된다.
![그림 4  디지털 서명의 삽입_edited](https://github.com/user-attachments/assets/5417ce23-5511-470b-ad03-b8a01707285f)
이처럼 반복적으로 서명을 삽입하는 방법은 잡음 및 신호 불안정 등 서명 훼손으로 인해 발생할 수 있는 문제점을 해결하기 위한 것으로 수신자 또한 N번 반복하여 추출한 이후 발신자의 인가 여부를 판단한다.
### Insert digital signature bitstream 
수신자는 N회 이전에 정상적인 서명이 추출 및 검증된다면 인가된 기관으로부터 발신된 전화로 판단하고 다음은 추출하지 않으며, N회 모두 검출한 이후 서명이 발견되지 않으면 공격자(비인가된 기관)로 판단한다.
![그림 5  디지털 서명의 추출_edited](https://github.com/user-attachments/assets/2ddc98ae-5190-4c4d-ae04-eeb1ca752afa)

 
## Performance
실시간 통신 환경에서 수신자가 수신한 전화의 발신지가 인가된 금융기관인지 아닌지 판별해내는데 걸리는 평균 시간과 정확성을 보인다.
다음은 소음이 미미한 정도인 실내 소음 기준 (NC, Noise Criteria) 40~50, 50dB(A) 수준의 환경에서 각 500회의 시행 평균을 나타낸 표이다.
|발신자|판별에 걸린 시간 (sec)|정확도|
|:---:|:---:|:---:|
|인가된 기관|4.1368|100%|
|공격자|3.9533|100%|

500회 시행 표본 평균에 따르면 

<b>[검출 소요 시간 평균]</b> = 1.75 sec

<b>[추출 소요 시간 평균]</b> = 1.2 sec

<b>[검증 소요 시간 평균]</b> = 0.1 sec

<b>검출 소요 시간</b>은 음성 데이터 내에 서명의 존재 여부를 판단하는 데 걸리는 시간을 의미하며, <b>추출 소요 시간</b>은 해당 음성에서 실질적인 데이터를 추출하는 데 걸리는 시간을 의미한다. <b>검증 소요 시간</b>은 Digital signature의 Data 검증에 걸리는 시간을 의미한다.
