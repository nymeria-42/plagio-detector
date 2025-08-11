from app.compare import lexical_topk, semantic_topk


def test_lexical_returns_list():
    res = lexical_topk("palavras de exemplo", k=2)
    assert isinstance(res, list)
    assert len(res) == 2


def test_semantic_returns_list():
    res = semantic_topk("um texto qualquer", k=2)
    assert isinstance(res, list)
    assert len(res) == 2