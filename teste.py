"""
Propriedades do `st.text_input`:
1. **label** (str): O rótulo exibido acima do campo de entrada de texto.
2. **value** (str, opcional): O valor padrão exibido no campo de entrada. O padrão é uma string vazia.
3. **max_chars** (int, opcional): O número máximo de caracteres permitidos no campo de entrada.
4. **key** (str, opcional): Uma chave única para identificar o widget. Útil para preservar o estado entre execuções.
5. **type** (str, opcional): Define o tipo de entrada. Pode ser:
    - `"default"`: Entrada de texto padrão.
    - `"password"`: Oculta o texto digitado, útil para senhas.
6. **placeholder** (str, opcional): Um texto de espaço reservado exibido no campo quando ele está vazio.
7. **help** (str, opcional): Um texto de ajuda exibido ao lado do campo de entrada.
8. **on_change** (callable, opcional): Uma função de callback chamada quando o valor do campo muda.
9. **args** (tuple, opcional): Argumentos posicionais passados para a função de callback `on_change`.
10. **kwargs** (dict, opcional): Argumentos nomeados passados para a função de callback `on_change`.
11. **disabled** (bool, opcional): Define se o campo de entrada está desabilitado. O padrão é `False`.
12. **label_visibility** (str, opcional): Controla a visibilidade do rótulo. Pode ser:
     - `"visible"`: O rótulo é exibido (padrão).
     - `"hidden"`: O rótulo não é exibido, mas ainda está disponível para leitores de tela.
     - `"collapsed"`: O rótulo é completamente oculto.
Retorno:
- **str**: O valor atual do campo de entrada.
"""