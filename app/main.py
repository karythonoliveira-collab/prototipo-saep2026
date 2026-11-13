from contextlib import asynccontextmanager
import sqlite3
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Query
from app.database import conectar, preparar_banco
from app.schemas import ProdutoEntrada, ProdutoEdicao, MovimentacaoEntrada

@asynccontextmanager
async def lifespan(app: FastAPI):
    preparar_banco()
    yield

app = FastAPI(
    title="Controle de Estoque - SAEP",
    version="1.0.0",
    lifespan=lifespan
)

def resultado(linha):
    return dict(linha) if linha else None

def buscar_produto(conexao,id_produto):
    item = conexao.execute('SELECT * FROM produto WHERE id_produto = ?', (id_produto,)).fetchone()
    if not item:
        raise HTTPException(status_code=404,detail='Produto não encontrado')
    return item

def produto_com_total(linha):
    item = resultado(linha)
    item['valor_total'] = round(float(Decimal(str(item['valor_unitario']))* item['quantidade_estoque']),2)
    return item

@app.get('/', tags=['Geral'])
def inicio():
    return {'mensagem': 'API de estoque funcionando', 'documento': '/docs', 'view': '/estoque'}

@app.get('/saude', tags=['Geral'])
def saude():
    return {'status':'ok'}

@app.post('/produtos', status_code=201, tags=['Produtos'])
def criar_produtos(dados: ProdutoEntrada):
    nome = dados.nome.strip()
    if not nome:
        raise HTTPException(422, 'O nome não pode ficar vazio')
    try:
        with conectar() as conn:
            cursor = conn.execute('''INSERT INTO produto (nome,quantidade_estoque, valor_unitario, estoque_minimo)
                                     VALUES (?,?,?,?)''',
                                     (nome,dados.quantidade_estoque, float(dados.valor_unitario), dados.estoque_minimo))
            return produto_com_total(buscar_produto(conn, cursor.lastrowid))
    except sqlite3.IntegrityError:
        raise HTTPException(409, 'Já existe um produto com esse nome')
@app.get('/produtos',tags=['Produtos'])
def listar_produtos():
    with conectar() as conn:
        return [produto_com_total(item) for item in conn.execute('SELECT * FROM produto ORDER BY nome')]

@app.get('/produtos/{id_produto}', tags=['Produtos'])
def obter_produto(id_produto: int):
    with conectar() as conn:
        return produto_com_total(buscar_produto(conn, id_produto))


@app.put('/produtos/{id_produto}', tags=['Produtos'])
def editar_produto(id_produto: int, dados: ProdutoEdicao):
    nome = dados.nome.strip()
    if not nome:
        raise HTTPException(422, 'O nome não pode ficar vazio')
    try:
        with conectar() as conn:
            buscar_produto(conn, id_produto)
            conn.execute('UPDATE produto SET nome = ?, valor_unitario = ?, estoque_minimo = ? WHERE id_produto = ?',
                         (nome, float(dados.valor_unitario), dados.estoque_minimo, id_produto))
            return produto_com_total(buscar_produto(conn, id_produto))
    except sqlite3.IntegrityError:
        raise HTTPException(409, 'Já existe um produto com esse nome')


@app.delete('/produtos/{id_produto}', tags=['Produtos'])
def excluir_produto(id_produto: int):
    with conectar() as conn:
        buscar_produto(conn, id_produto)
        if conn.execute('SELECT 1 FROM movimentacao WHERE id_produto = ? LIMIT 1', (id_produto,)).fetchone():
            raise HTTPException(409, 'Este produto possui movimentações e não pode ser excluído')
        conn.execute('DELETE FROM produto WHERE id_produto = ?', (id_produto,))
    return {'mensagem': 'Produto excluído'}


@app.post('/movimentacoes', status_code=201, tags=['Movimentações'])
def movimentar_estoque(dados: MovimentacaoEntrada):
    with conectar() as conn:
        # Transação garante que saldo e histórico sejam alterados juntos.
        conn.execute('BEGIN IMMEDIATE')
        produto = buscar_produto(conn, dados.id_produto)
        saldo_atual = produto['quantidade_estoque']
        if dados.tipo == 'SAIDA' and dados.quantidade > saldo_atual:
            raise HTTPException(422, 'Quantidade maior que o estoque disponível')
        novo_saldo = saldo_atual + dados.quantidade if dados.tipo == 'ENTRADA' else saldo_atual - dados.quantidade
        cursor = conn.execute('INSERT INTO movimentacao (tipo, quantidade, id_produto) VALUES (?, ?, ?)',
                              (dados.tipo, dados.quantidade, dados.id_produto))
        conn.execute('UPDATE produto SET quantidade_estoque = ? WHERE id_produto = ?', (novo_saldo, dados.id_produto))
        return {'id_movimentacao': cursor.lastrowid, 'tipo': dados.tipo, 'quantidade': dados.quantidade,
                'id_produto': dados.id_produto, 'saldo_atual': novo_saldo}


@app.get('/movimentacoes', tags=['Movimentações'])
def listar_movimentacoes(tipo: str | None = Query(default=None, pattern='^(ENTRADA|SAIDA)$')):
    sql = '''SELECT m.id_movimentacao, m.tipo, m.quantidade, m.datetime_movimentacao,
                    m.id_produto, p.nome AS produto
             FROM movimentacao m JOIN produto p ON p.id_produto = m.id_produto'''
    valores = ()
    if tipo:
        sql += ' WHERE m.tipo = ?'
        valores = (tipo,)
    sql += ' ORDER BY m.id_movimentacao DESC'
    with conectar() as conn:
        return [resultado(l) for l in conn.execute(sql, valores)]


@app.get('/saidas', tags=['Movimentações'])
def listar_saidas():
    return listar_movimentacoes('SAIDA')


@app.delete('/movimentacoes/{id_movimentacao}', tags=['Movimentações'])
def excluir_movimentacao(id_movimentacao: int):
    with conectar() as conn:
        conn.execute('BEGIN IMMEDIATE')
        mov = conn.execute('SELECT * FROM movimentacao WHERE id_movimentacao = ?', (id_movimentacao,)).fetchone()
        if not mov:
            raise HTTPException(404, 'Movimentação não encontrada')
        produto = buscar_produto(conn, mov['id_produto'])
        saldo = produto['quantidade_estoque']
        # Excluir uma entrada desfaz a entrada; excluir uma saída devolve as unidades.
        saldo_novo = saldo - mov['quantidade'] if mov['tipo'] == 'ENTRADA' else saldo + mov['quantidade']
        if saldo_novo < 0:
            raise HTTPException(409, 'Não é possível desfazer esta entrada: estoque insuficiente')
        conn.execute('UPDATE produto SET quantidade_estoque = ? WHERE id_produto = ?', (saldo_novo, mov['id_produto']))
        conn.execute('DELETE FROM movimentacao WHERE id_movimentacao = ?', (id_movimentacao,))
        return {'mensagem': 'Movimentação excluída e saldo corrigido', 'saldo_atual': saldo_novo}


@app.get('/estoque', tags=['Estoque / VIEW'])
def verificar_estoque():
    """Consulta a VIEW criada no SQLite."""
    with conectar() as conn:
        return [resultado(l) for l in conn.execute('SELECT * FROM vw_situacao_estoque ORDER BY nome')]


@app.get('/estoque/baixo', tags=['Estoque / VIEW'])
def estoque_baixo():
    with conectar() as conn:
        return [resultado(l) for l in conn.execute(
            "SELECT * FROM vw_situacao_estoque WHERE situacao IN ('Baixo', 'Sem estoque') ORDER BY nome")]


@app.get('/estoque/resumo', tags=['Estoque / VIEW'])
def resumo_estoque():
    with conectar() as conn:
        dados = conn.execute('''SELECT COUNT(*) AS produtos, COALESCE(SUM(saldo), 0) AS unidades,
                              COALESCE(SUM(valor_total), 0) AS valor_total,
                              SUM(CASE WHEN situacao != 'Normal' THEN 1 ELSE 0 END) AS precisam_repor
                              FROM vw_situacao_estoque''').fetchone()
        item = resultado(dados)
        item['precisam_repor'] = item['precisam_repor'] or 0
        return item
