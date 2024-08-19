import streamlit as st
from itertools import product
import random

def make_reflexive(X, R): 
    R_new = list(R)
    for a in X: 
        R_new.append((a,a))
    return set(R_new)

def make_irreflexive(X, R): 
    R_new = list()
    for a, b in R:
        if a != b: 
            R_new.append((a,b))
    return set(R_new)

def make_symmetric(R): 
    R_new = list(R)
    for a, b in R: 
        R_new.append((b,a))
    return set(R_new)

def make_asymmetric(R): 
    R_new = list()
    for a, b in R: 
        if (b, a) not in R_new:
            R_new.append((a, b))
    return set(R_new)

def make_transitive(X, R):
    R_new = list()
    for a in X: 
        for b in X: 
            for c in X:
                if (a, b) in R and (b,c) in R:
                    R_new += [(a, b), (b, c), (a, c)]
    return set(R_new)
    

def generate_relation(Xs):
    """Return a relation on X"""

    X = random.sample(Xs, random.choice([3, 4]))

    num_init_pairs = random.choice([3, 4, 4, 5, 5, 5, 5, 6, 6, 7, 8])
    pairs = list(product(X, repeat=2))
    R = list()
    for _ in range(num_init_pairs):
        R.append(random.choice(pairs))

    if random.choice([True] * 2 + [False]): 
        R = make_transitive(X, R)
    if random.choice([True, False]): 
        R = make_asymmetric(R)
    elif random.choice([True, False]): 
        R = make_symmetric(R)
    if random.choice([True, False]): 
        R = make_irreflexive(X, R)
    elif random.choice([True, False]): 
        R = make_reflexive(X, R)
    
    return X, set(R)


def is_reflexive(X, R):
    counter_examples = list()
    for a in X: 
        if (a, a) not in R: 
            counter_examples.append(f'not-${a}' + '\\mathrel{R}' + f'{a}$')
    return len(counter_examples) == 0, counter_examples

def is_irreflexive(X, R):
    counter_examples = list()
    for a in X: 
        if (a, a) in R: 
            counter_examples.append(f'${a}' + '\\mathrel{R}' + f'{a}$')
    return len(counter_examples) == 0, counter_examples

def is_symmetric(R):
    counter_examples = list()
    for a, b in R: 
        if (b, a) not in R: 
            counter_examples.append(f'${a}' + '\\mathrel{R}' + f'{b}$ but not-' + f'${b}' + '\\mathrel{R}' + f'{a}$')
    return len(counter_examples) == 0, counter_examples
def is_asymmetric(R):
    counter_examples = list()
    for a, b in R: 
        if (b, a)  in R: 
            counter_examples.append(f'${a}' + '\\mathrel{R}' + f'{b}$ and ' + f'${b}' + '\\mathrel{R}' + f'{a}$')
    return len(counter_examples) == 0, counter_examples

def is_connected(X, R):
    counter_examples = list()
    for a in X:
        for b in X:
            if (a, b) not in R and (b, a) not in R: 
                if a == b: 
                    counter_examples.append(f'not-${a}' + '\\mathrel{R}' + f'{b}$')
                else: 
                    counter_examples.append(f'not-${a}' + '\\mathrel{R}' + f'{b}$ and not-' + f'${b}' + '\\mathrel{R}' + f'{a}$')
    return len(counter_examples) == 0, counter_examples

def is_transitive(X, R):
    counter_examples = list()
    for a in X:
        for b in X: 
            for c in X: 
                if (a, b) in R and (b, c) in R and (a, c) not in R: 
                    counter_examples.append(f'${a}' + '\\mathrel{R}' + f'{b}$ and ' + f'${b}' + '\\mathrel{R}' + f'{c}$, but  not-' + f'${a}' + '\\mathrel{R}' + f'{c}$')
    return len(counter_examples) == 0, counter_examples

a = 0
b = 1
c = 2
d = 3
e = 4

Xs = [a, b, c, d, e]

def display_relation(R):
    pairs = sorted(list(R))
    if len(pairs) == 0: 
        return '\\varnothing'
    latex_str = ''
    latex_str += '\{'
    for x,y in pairs: 
        latex_str += f'({x}, {y}), '
    return latex_str[:-2] + '\}'

def display_set(X):
    elems = sorted(list(X))
    latex_str = ''
    latex_str += '\{'
    for x in elems: 
        latex_str += f'{x}, '
    return latex_str[:-2] + '\}'

def generate_graph_viz_chart(Xs, R): 
    graphviz_str = 'digraph {\n'
    for a in Xs: 
        graphviz_str += f'{a}\n'
    for a, b in R: 
        graphviz_str += f'{a} -> {b}\n'

    graphviz_str += '}'
    return graphviz_str

if 'rel' not in st.session_state or 'X' not in st.session_state: 
    X, R = generate_relation(Xs)
    st.session_state.X = X
    st.session_state.rel = R

f"""
Suppose that 
* $X={display_set(st.session_state.X)}$
* $R={display_relation(st.session_state.rel)}$
"""

show_rel = st.checkbox('Display Relation')

if show_rel:
    st.graphviz_chart(f"{generate_graph_viz_chart(st.session_state.X, st.session_state.rel)}")

with st.form("my_form"):
    st.write("Select all the properties satisfied by this relation.")
    col1, col2, col3 = st.columns(3)
    with col1: 
        trans = st.checkbox("Transitive")
    with col2: 
        symm = st.checkbox("Symmetric")
        asymm = st.checkbox("Asymmetric")
    with col3: 
        refl = st.checkbox("Reflexive")
        irrefl = st.checkbox("Irreflexive")

    submitted = st.form_submit_button("Check Answer")
    if submitted:
        is_refl, refl_exs = is_reflexive(st.session_state.X, st.session_state.rel)
        is_trans, trans_exs = is_transitive(st.session_state.X, st.session_state.rel)
        is_symm, symm_exs = is_symmetric(st.session_state.rel)
        is_asymm, asymm_exs = is_asymmetric(st.session_state.rel)
        is_irrefl, irrefl_exs = is_irreflexive(st.session_state.X, st.session_state.rel)

        prop = 'transitive'
        user_val = trans
        answer_val = is_trans
        expls = trans_exs
        if user_val and answer_val:
            st.success(f'Correct, the relation is {prop}.') 
        if not user_val and not answer_val:
            st.success(f'Correct, the relation is not {prop}.') 
        elif user_val and not answer_val: 
            st.warning(f"Incorrect, the relation is not {prop}.")
            for ex_str in expls: 
                st.write("* " + ex_str)
        elif not user_val and  answer_val: 
            st.warning(f"Incorrect, the relation is {prop}.")

        prop = 'symmetric'
        user_val = symm
        answer_val = is_symm
        expls = symm_exs
        if user_val and answer_val:
            st.success(f'Correct, the relation is {prop}.') 
        if not user_val and not answer_val:
            st.success(f'Correct, the relation is not {prop}.') 
        elif user_val and not answer_val: 
            st.warning(f"Incorrect, the relation is not {prop}.")
            for ex_str in expls: 
                st.write("* " + ex_str)
        elif not user_val and  answer_val: 
            st.warning(f"Incorrect, the relation is {prop}.")

        prop = 'asymmetric'
        user_val = asymm
        answer_val = is_asymm
        expls = asymm_exs
        if user_val and answer_val:
            st.success(f'Correct, the relation is {prop}.') 
        if not user_val and not answer_val:
            st.success(f'Correct, the relation is not {prop}.') 
        elif user_val and not answer_val: 
            st.warning(f"Incorrect, the relation is not {prop}.")
            for ex_str in expls: 
                st.write("* " + ex_str)
        elif not user_val and  answer_val: 
            st.warning(f"Incorrect, the relation is {prop}.")

        prop = 'reflexive'
        user_val = refl
        answer_val = is_refl
        expls = refl_exs
        if user_val and answer_val:
            st.success(f'Correct, the relation is {prop}.') 
        if not user_val and not answer_val:
            st.success(f'Correct, the relation is not {prop}.') 
        elif user_val and not answer_val: 
            st.warning(f"Incorrect, the relation is not {prop}.")
            for ex_str in expls: 
                st.write("* " + ex_str)
        elif not user_val and answer_val: 
            st.warning(f"Incorrect, the relation is {prop}.")

        prop = 'irreflexive'
        user_val = irrefl
        answer_val = is_irrefl
        expls = irrefl_exs
        if user_val and answer_val:
            st.success(f'Correct, the relation is {prop}.') 
        if not user_val and not answer_val:
            st.success(f'Correct, the relation is not {prop}.') 
        elif user_val and not answer_val: 
            st.warning(f"Incorrect, the relation is not {prop}.")
            for ex_str in expls: 
                st.write("* " + ex_str)
        elif not user_val and answer_val: 
            st.warning(f"Incorrect, the relation is {prop}.")

if st.button("Generate another relation"):
    X, R = generate_relation(Xs)
    st.session_state.X = X
    st.session_state.rel = R
    st.rerun()
