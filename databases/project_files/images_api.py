##VARIABLES
##    expression
##    order_by
##    limit_number
##    
##
##
##SELECT * FROM photos WHERE expression ORDER BY order DESC LIMIT limit
class Photos():
    def __init__(self):
        self.photos = []
    
    def getpics(self, expression, order, limit):
        curs.execute("SELECT url FROM photos WHERE '{}' ORDER BY '{}' DESC LIMIT '{}';").format(express, order, limit)
        self.photos = curs.fetchall()
        return self.photos

expression = "cat"
blah = Photo()
result = Photo().expression 
print(result)
print(expression)
