import pandas as pd

def apply_bollinger(df, window=20):
    # 1. Close 데이터 추출
    if 'Close' not in df or len(df) < window:
        raise ValueError("유효한 'Close' 데이터가 부족하거나 누락됨")

    close = df['Close'].copy()

    # 2. 볼린저 밴드 계산
    ma = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    upper = ma + 2 * std
    lower = ma - 2 * std

    # 3. DataFrame 생성 (NaN 포함 상태로 먼저 생성)
    result = pd.concat([close, ma, upper, lower], axis=1)
    result.columns = ['Close', 'MA', 'Upper', 'Lower']

    # 4. NaN 제거 (rolling 때문에 앞부분은 버려짐)
    result.dropna(inplace=True)

    # 5. 시그널 계산
    result['Buy'] = result['Close'] < result['Lower']
    result['Sell'] = result['Close'] > result['Upper']

    return result
