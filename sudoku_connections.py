from graph import Graph

class SudokuConnections : 
    def __init__(self, size) :  # constructor

        self.graph = Graph() # Graph Object

        if size != 9 and size != 16:
            raise ValueError("Size can only be 9 or 16")

        self.rows = size
        self.cols = size
        self.size = size
        self.total_blocks = self.rows*self.cols #256

        self.__generateGraph() # Generates all the nodes
        self.connectEdges() # connects all the nodes acc to sudoku constraints

        self.allIds = self.graph.getAllNodesIds() # storing all the ids in a list

        

    def __generateGraph(self) : 
        """
        Generates nodes with id from 1 to 81.
        Both inclusive
        """
        for idx in range(1, self.total_blocks+1) : 
            _ = self.graph.addNode(idx)

    def connectEdges(self) : 
        """
        Connect nodes according to Sudoku Constraints : 

        # ROWS

       from start of each id number connect all the 
       successive numbers till you reach a multiple of 9


        # COLS (add 9 (+9))

        from start of id number. +9 for each connection
        till you reach a number >= 73 and <= 81

        # BLOCKS
        Connect all the elements in the block which do not 
        come in the same column or row.
        1   2   3
        10  11  12
        19  20  21

        1 -> 11, 12, 20, 21
        2 -> 10, 19, 12, 21
        3 -> 10, 11, 19, 20 
        Similarly for 10, 11, 12, 19, 20, 21.

        """
        matrix = self.__getGridMatrix()

        head_connections = dict() # head : connections

        for row in range(self.rows) :
            for col in range(self.cols) : 
                
                head = matrix[row][col] #id of the node
                connections = self.__whatToConnect(matrix, row, col)
                
                head_connections[head] = connections
        # connect all the edges

        self.__connectThose(head_connections=head_connections)
        
    def __connectThose(self, head_connections) : 
        for head in head_connections.keys() : #head is the start idx
            connections = head_connections[head]
            for key in connections :  #get list of all the connections
                for v in connections[key] : 
                    self.graph.addEdge(src=head, dst=v)

 
    def __whatToConnect(self, matrix, rows, cols) :

        """
        matrix : stores the id of each node representing each cell

        returns dictionary

        connections - dictionary
        rows : [all the ids in the rows]
        cols : [all the ids in the cols]
        blocks : [all the ids in the block]
        
        ** to be connected to the head.
        """
        connections = dict()

        row = []
        col = []
        block = []

        # ROWS
        for c in range(cols+1, self.cols) : 
            row.append(matrix[rows][c])
        
        connections["rows"] = row

        # COLS 
        for r in range(rows+1, self.rows):
            col.append(matrix[r][cols])
        
        connections["cols"] = col

        # BLOCKS
        if self.size == 16:
            if rows%4 == 0 : 

                if cols%4 == 0 :
                    
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+1][cols+3])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+2][cols+2])
                    block.append(matrix[rows+2][cols+3])
                    block.append(matrix[rows+3][cols+1])
                    block.append(matrix[rows+3][cols+2])
                    block.append(matrix[rows+3][cols+3])

                elif cols%4 == 1 :
                    
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+2][cols+2])
                    block.append(matrix[rows+3][cols-1])
                    block.append(matrix[rows+3][cols+1])
                    block.append(matrix[rows+3][cols+2])
                    
                elif cols%4 == 2 :
                    
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+2][cols-2])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+3][cols-2])
                    block.append(matrix[rows+3][cols-1])
                    block.append(matrix[rows+3][cols+1])
                
                elif cols%4 == 3 :
                    
                    block.append(matrix[rows+1][cols-3])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+2][cols-3])
                    block.append(matrix[rows+2][cols-2])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+3][cols-3])
                    block.append(matrix[rows+3][cols-2])
                    block.append(matrix[rows+3][cols-1])


            elif rows%4 == 1 :
                
                if cols%4 == 0 :
                    
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows-1][cols+3])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+1][cols+3])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+2][cols+2])
                    block.append(matrix[rows+2][cols+3])

                elif cols%4 == 1 :
                    
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+2][cols+2])
                    
                elif cols%4 == 2 :
                    
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+2][cols-2])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+2][cols+1])
                
                elif cols%4 == 3 :
                    
                    block.append(matrix[rows-1][cols-3])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows+1][cols-3])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+2][cols-3])
                    block.append(matrix[rows+2][cols-2])
                    block.append(matrix[rows+2][cols-1])

            elif rows%4 == 2 :
                
                if cols%4 == 0 :
                    
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-2][cols+2])
                    block.append(matrix[rows-2][cols+3])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows-1][cols+3])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+1][cols+3])

                elif cols%4 == 1 :
                    
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-2][cols+2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    
                elif cols%4 == 2 :
                    
                    block.append(matrix[rows-2][cols-2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                
                elif cols%4 == 3 :
                    
                    block.append(matrix[rows-2][cols-3])
                    block.append(matrix[rows-2][cols-2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-1][cols-3])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows+1][cols-3])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])

            elif rows%4 == 3 :
                
                if cols%4 == 0 :
                    
                    block.append(matrix[rows-3][cols+1])
                    block.append(matrix[rows-3][cols+2])
                    block.append(matrix[rows-3][cols+3])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-2][cols+2])
                    block.append(matrix[rows-2][cols+3])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows-1][cols+3])

                elif cols%4 == 1 :
                    
                    block.append(matrix[rows-3][cols-1])
                    block.append(matrix[rows-3][cols+1])
                    block.append(matrix[rows-3][cols+2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-2][cols+2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    
                elif cols%4 == 2 :
                    
                    block.append(matrix[rows-3][cols-2])
                    block.append(matrix[rows-3][cols-1])
                    block.append(matrix[rows-3][cols+1])
                    block.append(matrix[rows-2][cols-2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                
                elif cols%4 == 3 :
                    
                    block.append(matrix[rows-3][cols-3])
                    block.append(matrix[rows-3][cols-2])
                    block.append(matrix[rows-3][cols-1])
                    block.append(matrix[rows-2][cols-3])
                    block.append(matrix[rows-2][cols-2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-1][cols-3])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
        elif self.size == 9:
            if rows%3 == 0 : 

                if cols%3 == 0 :
                    
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])
                    block.append(matrix[rows+2][cols+1])
                    block.append(matrix[rows+2][cols+2])

                elif cols%3 == 1 :
                    
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+2][cols-1])
                    block.append(matrix[rows+2][cols+1])
                    
                elif cols%3 == 2 :
                    
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+2][cols-2])
                    block.append(matrix[rows+2][cols-1])

            elif rows%3 == 1 :
                
                if cols%3 == 0 :
                    
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])
                    block.append(matrix[rows+1][cols+1])
                    block.append(matrix[rows+1][cols+2])

                elif cols%3 == 1 :
                    
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows+1][cols-1])
                    block.append(matrix[rows+1][cols+1])
                    
                elif cols%3 == 2 :
                    
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows+1][cols-2])
                    block.append(matrix[rows+1][cols-1])

            elif rows%3 == 2 :
                
                if cols%3 == 0 :
                    
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-2][cols+2])
                    block.append(matrix[rows-1][cols+1])
                    block.append(matrix[rows-1][cols+2])

                elif cols%3 == 1 :
                    
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-2][cols+1])
                    block.append(matrix[rows-1][cols-1])
                    block.append(matrix[rows-1][cols+1])
                    
                elif cols%3 == 2 :
                    
                    block.append(matrix[rows-2][cols-2])
                    block.append(matrix[rows-2][cols-1])
                    block.append(matrix[rows-1][cols-2])
                    block.append(matrix[rows-1][cols-1])

        connections["blocks"] = block
        return connections

    def __getGridMatrix(self) : 
        """
        Generates the 9x9 grid or matrix consisting of node ids.
        
        This matrix will act as amapper of each cell with each node 
        through node ids
        """
        matrix = [[0 for cols in range(self.cols)] 
        for rows in range(self.rows)]

        count = 1
        for rows in range(self.rows) :
            for cols in range(self.cols):
                matrix[rows][cols] = count
                count+=1
        return matrix

"""
TESTING
"""       
def test_connections() : 
    sudoku = SudokuConnections()
    sudoku.connectEdges()
    print("All node Ids : ")
    print(sudoku.graph.getAllNodesIds())
    print()
    for idx in sudoku.graph.getAllNodesIds() : 
        print(idx, "Connected to->", sudoku.graph.allNodes[idx].getConnections())

if __name__ == "__main__" : 
    test_connections()