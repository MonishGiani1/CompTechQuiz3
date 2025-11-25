START_SYMBOL = 'C'

NONTERMINALS = {'C', 'A', 'T', 'E'}

TERMINALS = {'f', '(', ')', ',', 'x', 'y'}

# LL(1) parse table:
PARSE_TABLE = {
    'C': {
        'f': ['f', '(', 'A', ')']
    },
    'A': {
        'x': ['E', 'T'],
        'y': ['E', 'T'],
        ')': ['ε']
    },
    'T': {
        ',': [',', 'E', 'T'],
        ')': ['ε']
    },
    'E': {
        'x': ['x'],
        'y': ['y']
    }
}

def parse_ll1(tokens: list[str], verbose: bool = False) -> str:
    """
    LL(1) table-driven predictive parser.
    tokens: list of tokens, e.g. ['i', '+', 'i', '$']
    Returns "ACCEPT" or "ERROR".
    """
    # ensure end marker
    if not tokens or tokens[-1] != '$':
        tokens = tokens + ['$']
    
    stack = ['$', START_SYMBOL]
    idx = 0  # index into tokens
    step = 1
    
    if verbose:
        print(f"{'Step':<4} {'Stack':<20} {'Input':<20} Action")
        print("-" * 60)
    
    while True:
        top = stack[-1]
        lookahead = tokens[idx]
        
        if verbose:
            stack_str = ' '.join(stack)
            input_str = ' '.join(tokens[idx:])
        
        # ACCEPT condition
        if top == '$' and lookahead == '$':
            if verbose:
                print(f"{step:<4} {stack_str:<20} {input_str:<20} ACCEPT")
            return "ACCEPT"
        
        # If top is terminal
        if top in TERMINALS or top == '$':
            if top == lookahead:
                stack.pop()
                idx += 1
                if verbose:
                    print(f"{step:<4} {stack_str:<20} {input_str:<20} match '{top}'")
            else:
                if verbose:
                    print(f"{step:<4} {stack_str:<20} {input_str:<20} ERROR (expected '{top}')")
                return "ERROR"
        
        # If top is nonterminal
        elif top in NONTERMINALS:
            table_row = PARSE_TABLE.get(top, {})
            production = table_row.get(lookahead)
            
            if production is None:
                if verbose:
                    print(f"{step:<4} {stack_str:<20} {input_str:<20} ERROR (no rule for {top}, {lookahead})")
                return "ERROR"
            
            stack.pop()
            rhs = production
            if not (len(rhs) == 1 and rhs[0] == 'ε'):
                for symbol in reversed(rhs):
                    stack.append(symbol)
            
            if verbose:
                prod_str = f"{top} -> {' '.join(rhs)}"
                print(f"{step:<4} {stack_str:<20} {input_str:<20} {prod_str}")
        else:
            if verbose:
                print(f"{step:<4} {stack_str:<20} {input_str:<20} ERROR (unknown symbol '{top}')")
            return "ERROR"
        
        step += 1

if __name__ == "__main__":
    # Test cases
    print("Test 1 - Legitimate: f ( x , y , x )")
    result1 = parse_ll1(['f', '(', 'x', ',', 'y', ',', 'x', ')'], verbose=True)
    print(f"\nResult: {result1}\n")
    
    print("\nTest 2 - Illegitimate: f x , y )")
    result2 = parse_ll1(['f', 'x', ',', 'y', ')'], verbose=True)
    print(f"\nResult: {result2}")