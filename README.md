# blockchain

---

#### blockchain.py - blockchain의 기본 구조를 python으로 작성
#### server.py     - blockchain.py 에서 작성한 blockchain을 flask를 통해 웹브라우저로 확인가능

---

#### templates   
index.html - 초기 페이지(현재 blockchain의 block상황을 보여준다.
mine.html  - mining을 진행하여 채굴된 block의 정보를 보여준다.
transactions_new.html  - transaction을 추가할 수 있다. (mining 시 transaction 포함됨)
pending.html    - transactions_new에서 추가되었지만 mining되지않은 transaction을 보여준다.
