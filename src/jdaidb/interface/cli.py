from jdaidb.parser.core import Parser

class CLI:
    def __init__(self, parser: Parser):
        self.parser = parser
    
    """
    Public Functions
    """

    def run(self):
        print("----------------------")
        print(" welcome to jdaidb 🐱")
        print("----------------------")
        print("to exit, please type EXIT")

        while True:
            print("🐱 ", end="")
            user_input = str(input())
            try:
                if user_input.upper() == "EXIT":
                    break
                elif user_input == "":
                    continue
                else:
                    self.parser.process(user_input)
            except Exception as e:
                print(f"an error has occurred. ({str(e)})")
        
        # delete parser and dependencies
        del self.parser
        
        print("jdaidb is successfully exited")
