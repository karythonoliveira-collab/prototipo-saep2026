1. Clone o repositório:
   ```bash
   git clone -b ArthurNunes https://github.com/karythonoliveira-collab/prototipo-saep2026/.git Saep26
   ```
2. Navegue até o diretório do projeto:
   ```bash
    cd Saep26
   ```
3. 
   3.1 Cria a .venv(windwos):
   ```bash
    py -m venv .venv 
   ```
   3.2 Cria a .venv:
   ```bash
    python3 -m venv .venv 
   ```
4. 
    4.1 ativa a venv(windwos):
    ```bash
    backend/.venv/Scripts/activate
   ```
   4.2 ativa a venv:
    ```bash
    source backend/.venv/Scripts/activate
   ```
5. Instalar biliotecas:
    ```bash
    cd backend; pip install -r requirements.txt
   ```

6.  Apos configura a .env excute para inicia o projeto:
    ```bash
    python -m uvicorn src.main:app --reload
   ```
   
