from lark import Lark, Tree
import json

grammar = r"""
start: query+
query: select_clause [put_clause] from_clause [where_clause] [";"]

select_clause: "ВЫБРАТЬ" field_list

put_clause: "ПОМЕСТИТЬ" temporary_table_name
temporary_table_name: NAME

from_clause: "ИЗ" source_list
field_list: field ("," field)*
field: NAME ["КАК" alias] 

source_list: source ("," source)*
source: NAME ["КАК" alias] | "(" query ")" ["КАК" alias]
alias: NAME

where_clause: "ГДЕ" condition
condition: left OP right
left: NAME
OP: "=" | ">" | "<" | "<>" | ">=" | "<="
right: NAME
NAME: /[А-Яа-яA-Za-z0-9_."\[\]&]+/

%ignore /\s+/
"""

parser = Lark(grammar, start="start")

text = """
ВЫБРАТЬ Товары.Номенклатура КАК Номенклатура, Товары.Количество КАК Количество ПОМЕСТИТЬ 312 ИЗ Справочники.Товары ГДЕ Количество > 10;
ВЫБРАТЬ ГруппыЗначений.ЗначениеДоступа ПОМЕСТИТЬ ЧЧЧ ИЗ Пидор ГДЕ ЗначениеДоступа = 5
"""

tree = parser.parse(text)
print(tree.pretty())

def extract_query_structure(tree):
    for clause in tree.children:
        if clause.data == "query":
                for case in clause.children:
                    if case.data == "select_clause":
                        select_fields = []
                        for fild in case.children[0].children:
                            field_name = fild.children[0]
                            alias = fild.children[1].children[0] if len(fild.children) > 1 else None
                            select_fields.append({"field": str(field_name), "alias": str(alias) if alias else None})

 

query_structure = extract_query_structure(tree)





