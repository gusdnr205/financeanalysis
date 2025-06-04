# 금융 분석

이 프로젝트는 볼린저 밴드를 이용해 금융 데이터를 분석하고 FastAPI 서버를 통해 실시간 조회와 간단한 백테스트 기능을 제공합니다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 사용법

FastAPI 서버를 실행합니다:

```bash
uvicorn server:app --reload
```

접속 후 다음 엔드포인트를 활용할 수 있습니다:

- `/analyze/{ticker}` – 지정한 종목의 최신 볼린저 밴드 신호 확인
- `/backtest/{ticker}` – 지정한 기간의 데이터를 사용해 백테스트 수행

## 실시간 거래 시뮬레이션

볼린저 밴드 신호를 이용한 실시간 거래 시뮬레이션을 실행하려면 다음 명령을 사용합니다:

```bash
python live_trading.py
```

스크립트는 `live_trading.log` 파일에 매수·매도 기록과 포트폴리오 가치를 남기며 콘솔에도 내용을 출력합니다.
