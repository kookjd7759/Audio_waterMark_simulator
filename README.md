# Audio_waterMark_simulator
음성 통신간 피싱 공격 방지를 위한 Realtime Audio Digital Signature System.

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
import or record an audio file (Audio file은 1 Channel 16,000Hz (.wav) 음성 파일이어야만 한다.)

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
Spread-spectrum 기법을 사용해 

 
## Performance
실시간 통신 환경에서 수신자가 수신한 전화의 발신지가 인가된 금융기관인지 아닌지 판별해내는데 걸리는 평균 시간과 정확성

소음이 미미한 환경에서 각 500회의 시행 평균을 나타낸 표
|발신자|판별에 걸린 시간 (sec)|정확도|
|:---:|:---:|:---:|
|인가된 기관|4.1368|100%|
|공격자|3.9533|100%|
