import sys
from importlib import reload
import formula

def parametrs_to_string(param):
    str_p = ""

    for item in param:
        str_p+=str(item)
        str_p+=','
    str_p = str_p[:-1]
    return  str_p


def execute(formula_name,parametrs):
    try:
        results = []
        parametrs_s = parametrs_to_string(parametrs)
        exec("reload(formula)")
        exec("reload(formula.{})".format(formula_name))
        exec("results.append(formula.{}.{}({}))".format(formula_name,formula_name,parametrs_s))
        return results[0]
    except:
        return None

if __name__ =="__main__":
    while True:
        print(execute(input("name:"),[int(input("a:")),input("b:")]))

