# Audio_waterMark_simulator
음성 통신간 피싱 공격 방지를 위한 Audio waterMark 기능을 시뮬레이션 하는 프로그램.

## 실행 화면
![화면 캡처 2024-07-23 162352](https://github.com/user-attachments/assets/aee2c5e3-192d-4462-b693-5cea9c81c09b)


## Menu

### Sound file
Sound file을 불러오거나 녹음하여 음성 파일을 선택(Sound file은 1Channel 16,000Hz (.wav) 음성 파일이어야만 함.)

### Watermark
[Create And insert] : 선택된 음성 파일에 waterMark 삽입

[Extract] : 선택된 음성 파일의 waterMark 검출

### Real Time Simulation
 - (setting) : Simulation의 mode 설정 기능, Caller가 인가된 금융 기관인지, 금융 기관을 사칭한 공격 단체인지 설정 가능

 - (Excution) : 위 설정으로 Simulation 실행
    - [Make a call] : 전화 통신 Simulation 시작
    - [hang up] : 전화 통신 Simulation 종료

Watermark 검출 및 미검출로 인한 인가된 금융 기관 판단 여부에 걸린 시간(Detect Time)과 판단 결과(Detect Result)를 표시

## Real Time insert / detect Algorithm
