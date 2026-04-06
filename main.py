#Andrew Stephens
#Project 2: Parser
#Dr. Ranjidha Rajan 
#Principles of Programming Languages
#Date: 04/5/2026

#imports the parser which allows the print statement to make calls to the other file.
import parser

#Ensures the loop continues
while True:
    try: #Takes input in the desired format
        text = input('INPUT: R@R > ')
        if not text.strip():
            continue
        
        #lexer = beta.Lexer("<stdin>", text)
        #takes the input as an argument and prints the tokens with specific index, coloumn, and row information
        lexer = parser.Lexer(text)
        tokens = lexer.make_tokens()
        print("\nTOKENS:")
        for t in tokens:
            print(t)

        #Creates an abstract syntax tree with division between left and right within the output
        parsed = parser.Parser(tokens)
        at = parsed.parse()
        print("\nABSTRACT SYNTAX TREE (AST):")
        parser.print_AST(at) 

    #Allows for catch all exception
    except Exception as e:
        print(f"\nPARSING ERROR: {e}")