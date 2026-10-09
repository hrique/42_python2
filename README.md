# Conceitos de exceções para a avaliação (lista 2)

Todos os exemplos foram testados no Python 3. Sempre que possível, uso o seu próprio código da lista 2.
A conferência do código (nomes, flake8, mypy) está em [lista2_revisao.md](lista2_revisao.md).

---

## 1. O que é uma exceção

- Uma **exceção** é um objeto que o Python cria quando algo dá errado durante a execução: `int("abc")`, `1 / 0`, abrir um arquivo que não existe.
- Se ninguém tratar, o programa **para** e mostra um **traceback**. É isso que o PDF chama de "crash", e a regra geral é: *"Your programs must never crash"*.
- **Comparação com C:** em C, quem dá erro devolve um código (`-1`, `NULL`) e você precisa conferir com `if` depois de **cada** chamada. Se esquecer, o programa segue com lixo. Em Python, o erro **não pode ser ignorado sem querer**: ou alguém trata, ou o programa para.

Analogia: o alarme de incêndio. Em C, cada sala tem uma lâmpada vermelha e você precisa olhar para ela. Em Python, o alarme toca e não para até alguém atender.

### Como ler um traceback

```
Traceback (most recent call last):
  File "tb.py", line 9, in <module>
    b()
  File "tb.py", line 6, in b
    return a()
  File "tb.py", line 2, in a
    return int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
```

- Leia **de baixo para cima**. A última linha diz o **tipo** (`ValueError`) e a **mensagem**.
- As linhas de cima mostram o caminho: `<module>` chamou `b`, que chamou `a`, onde o erro nasceu.

---

## 2. Propagação: a exceção "sobe" pelas funções

Quando uma exceção acontece, o Python **abandona a função na hora** e devolve o erro para quem a chamou. Se lá também não tiver `try`, sobe de novo, até achar um `except` que combine ou chegar no topo (crash).

```python
def a() -> int:
    return int("x")          # o erro nasce aqui

def b() -> int:
    return a()               # não trata, então só repassa

try:
    b()
except ValueError as e:
    print("pego no topo:", e)
# pego no topo: invalid literal for int() with base 10: 'x'
```

Analogia: batata quente. Quem não sabe o que fazer com ela passa para trás, até chegar em quem sabe.

**No seu código (ex0 e ex1):** `input_temperature` **não** tem `try`. Ela só converte e, se der erro, o erro sobe para `test_temperature`, que é quem trata. É a divisão certa: **quem detecta o problema** nem sempre é **quem sabe o que fazer** com ele.

---

## 3. `try` / `except` (ex0)

```python
try:
    x = input_temperature(value)        # pode dar erro
    print(f"Temperature is now {x}°C")  # só roda se a linha de cima deu certo
except ValueError as e:
    print(f"Caught input_temperature error: {e}")
```

Regras do fluxo:

1. O Python roda o `try` linha por linha.
2. Se uma linha dá erro, **o resto do `try` é pulado**. Por isso, com `"abc"`, o `print("Temperature is now...")` não aparece.
3. O Python procura o primeiro `except` cujo tipo combina com o erro e roda esse bloco.
4. Depois, o programa **continua normalmente** depois do `try`. É assim que o seu `for` testa o próximo valor.

- **`as e`** guarda o objeto da exceção na variável `e`.
- **`print(e)`** mostra a **mensagem** do erro (é o `str(e)`). Por isso a saída é `invalid literal for int() with base 10: 'abc'`, sem o nome `ValueError`.
- `e.args` é a tupla com o que foi passado ao criar o erro: `("invalid literal ...",)`.

**Pergunta provável:** "Por que `ValueError` e não `Exception`?" Porque `int()` com texto inválido gera `ValueError`. Pegar só o erro que você **espera** evita esconder bugs que você não esperava (ver seção 6).

---

## 4. `raise`: lançar o seu próprio erro (ex1)

`"100"` vira o número 100 sem problema, então o Python não reclama. Mas para o **seu programa** é um valor inválido. Quem decide isso é você, com `raise`:

```python
def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)            # pode lançar ValueError sozinho
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    elif temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    return temp
```

- **`raise`** cria a exceção e a lança. A função **para ali**: o `return temp` não roda.
- Por que **`ValueError`**? Porque o tipo do dado está certo (é um número), mas o **valor** não serve. É a mesma ideia de `int("abc")`: tipo certo (texto), valor ruim.
- Vantagem: o `"abc"` e o `"100"` caem **no mesmo `except ValueError`**. O `test_temperature` não precisa saber o motivo; ele só imprime a mensagem.
- Limites incluídos: `< 0` e `> 40` deixam o 0 e o 40 passarem, como o PDF pede ("limits included").

### `raise` sozinho: relançar

Dentro de um `except`, `raise` sem nada relança o **mesmo** erro para cima. Serve para registrar algo e deixar outra pessoa tratar:

```python
try:
    try:
        1 / 0
    except ZeroDivisionError:
        print("loga e relança")
        raise
except ZeroDivisionError as e:
    print("de fora:", e)
# loga e relança
# de fora: division by zero
```

---

## 5. Os tipos de erro do ex2

Cada tipo de erro descreve **um problema diferente**. É como os diagnósticos de um médico: "dor" é genérico, mas "fratura" e "febre" pedem tratamentos diferentes.

| Erro | Quando acontece | No seu ex2 | Mensagem |
|------|-----------------|------------|----------|
| `ValueError` | tipo certo, **valor** errado | `int("abc")` | `invalid literal for int() with base 10: 'abc'` |
| `ZeroDivisionError` | divisão (ou `%`) por zero | `1 / 0` | `division by zero` |
| `FileNotFoundError` | o arquivo não existe | `open("/non/existent/file", "r")` | `[Errno 2] No such file or directory: ...` |
| `TypeError` | operação com **tipos** que não combinam | `"text" + 1` | `can only concatenate str (not "int") to str` |

Outros que o PDF cita e podem cair em pergunta:

| Erro | Exemplo | Mensagem |
|------|---------|----------|
| `KeyError` | `{"a": 1}["b"]` | `'b'` |
| `IndexError` | `[1][5]` | `list index out of range` |
| `AttributeError` | `None.x` | `'NoneType' object has no attribute 'x'` |

**`ValueError` x `TypeError`** (pergunta clássica):
- `int("abc")` → `ValueError`: `int` aceita texto, mas **esse** texto não é um número.
- `int(None)` → `TypeError`: `int` não aceita `None` de jeito nenhum.
- `"text" + 1` → `TypeError`: `str` e `int` não se somam.

**Por que não precisa `close()` no `FileNotFoundError`?** Porque o `open()` falha **antes** de abrir. Não existe arquivo aberto para fechar.

**Por que o mypy reclama do `"text" + 1`?** O mypy olha o código **sem rodar** (análise estática) e vê que `str + int` é inválido. O PDF pede que você mantenha esse erro de propósito, porque é ele que gera o `TypeError` na execução. Isso mostra a diferença entre:
- **erro estático**: o mypy acha lendo o código;
- **erro em tempo de execução**: o Python acha rodando.

---

## 6. Hierarquia de exceções

Exceções são **classes**, e elas herdam umas das outras, igual à lista 1. A árvore resumida:

```
BaseException
 ├── KeyboardInterrupt        (Ctrl+C)
 ├── SystemExit               (exit())
 └── Exception                (quase todos os erros "normais")
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── KeyError
      │    └── IndexError
      ├── OSError
      │    └── FileNotFoundError
      ├── ValueError
      ├── TypeError
      ├── AttributeError
      └── GardenError          (a sua, do ex3)
           ├── PlantError
           └── WaterError
```

Testado no Python:
```python
[c.__name__ for c in ZeroDivisionError.__mro__]
# ['ZeroDivisionError', 'ArithmeticError', 'Exception', 'BaseException', 'object']
[c.__name__ for c in FileNotFoundError.__mro__]
# ['FileNotFoundError', 'OSError', 'Exception', 'BaseException', 'object']
```

**A regra que importa:** `except X` pega o erro `X` **e todas as filhas de `X`**. É o mesmo `isinstance` da lista 1: um `ZeroDivisionError` **é um** `ArithmeticError`, que **é uma** `Exception`.

- `except Exception` pega quase tudo. Útil como "rede de segurança", mas esconde bugs: um erro de digitação que vira `NameError` seria engolido em silêncio.
- `except BaseException` ou `except:` sozinho pegam até o **Ctrl+C** e o `exit()`. O programa fica impossível de interromper. **Evite.**
- Por isso `KeyboardInterrupt` não fica embaixo de `Exception`: para que um `except Exception` não impeça você de parar o programa.

### A ordem dos `except` importa

O Python testa os `except` **de cima para baixo** e usa o **primeiro** que combina. Se o mais genérico vier antes, o específico nunca roda:

```python
try:
    1 / 0
except Exception:            # pega aqui
    pass
except ZeroDivisionError:    # nunca chega aqui
    print("x")
```

Regra: **do mais específico para o mais genérico**.

---

## 7. Vários erros em um só `try` (ex2)

O PDF pergunta: *"How can you catch multiple types of errors with a single try: only?"* Existem duas formas, e você deve saber as duas.

**Forma 1, vários `except`** (a que você usou): um tratamento diferente para cada tipo.
```python
try:
    garden_operations(num)
except ValueError as e:
    print(f"Caught ValueError: {e}")
except ZeroDivisionError as e:
    print(f"Caught ZeroDivisionError: {e}")
```

**Forma 2, tupla**: o **mesmo** tratamento para vários tipos.
```python
try:
    [1][5]
except (KeyError, IndexError) as e:
    print("tupla:", e)
# tupla: list index out of range
```

O PDF proíbe `type(e)`. Por isso a forma 1 é a natural no ex2: cada `except` já sabe qual nome imprimir.

---

## 8. `else` no `try` (ex2)

```python
try:
    garden_operations(num)
except ...:
    ...
else:
    print("Operation completed successfully")
```

- O `else` roda **só se o `try` terminou sem erro**. No seu ex2, só a operação 4 chega lá.
- Por que não colocar o `print` no fim do `try`? Daria a mesma saída aqui, mas o `else` deixa o `try` só com o código que **pode falhar**. Assim um erro no `print` não seria confundido com um erro da operação.

---

## 9. Exceções personalizadas (ex3)

```python
class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)
```

Linha por linha:
- `class GardenError(Exception)`: toda exceção sua **precisa** herdar de `Exception` (direta ou indiretamente). Se a classe não herdar de nenhuma exceção, o `raise` dá `TypeError: exceptions must derive from BaseException`.
- `message: str = "..."`: **valor padrão**. Se você fizer `raise PlantError()` sem texto, a mensagem é `"Unknown plant error"`. É o que o PDF pede.
- `super().__init__(message)`: entrega a mensagem para o `__init__` de `Exception`, que a guarda em `e.args`. **É por isso que `print(e)` mostra o texto.**
- `PlantError(GardenError)`: `PlantError` **é um** `GardenError`, que **é uma** `Exception`.

Testado:
```python
print(PlantError())                         # Unknown plant error
isinstance(PlantError(), GardenError)       # True
isinstance(PlantError(), Exception)         # True
```

### Por que criar os seus próprios erros

1. **Clareza:** `PlantError` diz na hora qual parte do sistema falhou. `ValueError` poderia ser qualquer coisa.
2. **Controle:** quem chama pode tratar só os erros do jardim, sem pegar sem querer um `ValueError` de outra parte do código.
3. **Organização por herança:** `except GardenError` pega **todos** os erros do jardim de uma vez; `except PlantError` pega só os de planta. É o que o terceiro teste do seu ex3 demonstra.

Analogia: o hospital tem a ala de "ortopedia" (`GardenError`) e, dentro dela, "joelho" (`PlantError`) e "ombro" (`WaterError`). Você pode mandar o paciente para a ala inteira ou para o especialista.

**Quando usar um built-in e quando criar o seu?** Use o built-in quando ele descreve bem o problema (`ValueError` para temperatura fora da faixa). Crie o seu quando o erro é **do seu domínio** e alguém vai querer tratá-lo separado dos outros.

**Pergunta provável:** "E se `PlantError` não tivesse `__init__`?" Ele herdaria o do `GardenError`, e a mensagem padrão seria `"Unknown garden error"`. Funciona, mas perde a mensagem específica.

---

## 10. `finally`: limpeza que sempre acontece (ex4)

```python
print("Opening watering system")
try:
    for plant in plants:
        water_plant(plant)
except PlantError as e:
    print(f"Caught PlantError: {e}")
    print(".. ending tests and returning to main")
    return
finally:
    print("Closing watering system\n")
```

- O `finally` roda **sempre**: com erro, sem erro, e **até com `return`** dentro do `try` ou do `except`.
- No seu ex4, o `except` faz `return`, mas antes de a função sair o Python roda o `finally`. Por isso "Closing watering system" aparece nos dois testes.
- Roda até quando **nenhum `except` combina**. O erro continua subindo, mas o `finally` roda primeiro:

```python
try:
    try:
        1 / 0
    except ValueError:
        print("nunca")
    finally:
        print("finally mesmo sem except certo")
except ZeroDivisionError:
    print("subiu pra fora")
# finally mesmo sem except certo
# subiu pra fora
```

Analogia: desligar o fogão. Deu certo o jantar ou queimou tudo, você desliga o fogão **antes** de sair da cozinha.

**Para que serve na vida real?** Fechar arquivos, conexões, liberar recursos. Em C você teria que lembrar do `fclose`/`free` em **cada** caminho de saída. O `finally` garante isso num lugar só.

### A ordem completa

```python
try:
    int("7") + 1
except ValueError:
    print("nao")
else:
    print("else roda")
finally:
    print("finally roda")
# else roda
# finally roda
```

| Bloco | Quando roda |
|-------|-------------|
| `try` | sempre começa |
| `except` | só se deu erro **daquele tipo** |
| `else` | só se **não** deu erro |
| `finally` | **sempre**, por último |

### Pegadinha: `return` dentro do `finally`

```python
def g() -> int:
    try:
        return 1
    finally:
        return 2

g()   # 2
```

O `return` do `finally` **ganha** do `return` do `try` (e também apaga uma exceção que estivesse subindo). Por isso nunca se coloca `return` no `finally`.

### `with`: o `finally` pronto

Para arquivos, o Python tem o `with`, que fecha o arquivo sozinho, mesmo com erro. Por baixo, ele faz um `try/finally`. Isso cai na lista 4, mas vale saber que é a mesma ideia:

```python
with open("dados.txt") as f:
    texto = f.read()
# aqui o arquivo já está fechado, deu erro ou não
```

---

## 11. Duas filosofias: EAFP e LBYL

- **LBYL** ("Look Before You Leap", olhe antes de pular): confere tudo com `if` antes de agir. É o estilo de C.
- **EAFP** ("Easier to Ask Forgiveness than Permission", é mais fácil pedir desculpa do que permissão): tenta direto e trata o erro se der errado. É o estilo comum em Python.

O seu ex0 é EAFP: em vez de conferir se o texto só tem dígitos antes de converter, você chama `int()` e trata o `ValueError`. Vantagem: o próprio `int()` sabe melhor do que você o que é um número válido (sinal, espaços etc.).

---

## 12. Pedidos ao vivo comuns

1. **Adicionar mais um valor no teste do ex1** (ex.: `"40"` deve passar, `"41"` deve falhar).
2. **No ex2, trocar os `except` separados por um com tupla** e explicar o que se perde (o nome do erro impresso).
3. **No ex2, adicionar uma operação 5 com `KeyError` ou `IndexError`**.
4. **No ex3, criar um `SunError(GardenError)`** e mostrar que `except GardenError` também pega ele.
5. **No ex3, lançar `raise PlantError()` sem mensagem** e mostrar a mensagem padrão.
6. **Inverter a ordem dos `except`** (`GardenError` antes de `PlantError`) e explicar por que o específico deixa de rodar.
7. **No ex4, tirar o `finally`** e colocar o `print` depois do `try`: mostrar que, com o `return` do `except`, a mensagem de fechar some no teste inválido.

## Perguntas rápidas para treinar em voz alta

1. O que é uma exceção? O que acontece se ninguém tratar?
2. Como se lê um traceback?
3. Depois que uma linha do `try` dá erro, o resto do `try` roda?
4. O que o `as e` guarda? O que o `print(e)` mostra?
5. O que `raise` faz? A função continua depois dele?
6. Por que `ValueError` para temperatura fora da faixa?
7. Diferença entre `ValueError` e `TypeError`?
8. Por que o Python tem tipos diferentes de erro?
9. Como pegar vários tipos de erro com um só `try`? (duas formas)
10. Por que a ordem dos `except` importa?
11. Por que `except Exception` é perigoso? E `except:` sozinho?
12. Para que serve o `else` do `try`?
13. Por que a exceção personalizada herda de `Exception`?
14. O que `super().__init__(message)` faz na sua exceção?
15. Quando criar um erro próprio em vez de usar um do Python?
16. Como a herança ajuda a organizar os erros?
17. O `finally` roda quando tem `return` no `except`? E quando nenhum `except` combina?
18. Por que limpar recursos mesmo quando dá erro?
19. Por que o mypy reclama no ex2 e você não corrige?
20. Diferença entre o jeito de C (código de retorno) e o de Python (exceção)?
