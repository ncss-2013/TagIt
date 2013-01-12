from cgi import escape

class Node(object):
    def __init__(self): pass
    def render(self): pass

class GroupNode(Node):
    def __init__(self, children = None):
        self.children = children if children else []
    def render(self, context):
        return ''.join(child.render(context) for child in self.children)

class TextNode(Node):
    def __init__(self, content = ''):
        self.content = content
    def render(self, context):
        return self.content

class PythonNode(Node):
    def __init__(self, code = ''):
        self.code = code
    def render(self, context):
        return str(eval(self.code, {}, context)) if self.code else 'Not Implemented!'

class IfNode(Node):
    def __init__(self, predicate, true, false = ''):
        self.true = true
        self.false = false
        self.predicate = predicate
    def render(self, context):
        return self.true.render(context) if eval(self.predicate, {}, context) else (self.false.render(context) if self.false else '')

class IncludeNode(Node):
    def __init__(self, path): #, var_dict = None):
        self.path = path
        # self.var_dict = var_dict if var_dict else {}
    def render(self, context):
        # context.update(var_dict)
        return create(''.join(open(self.path).readlines()), context)

class ForNode(Node):
    def __init__(self, items, iterable, true, false = ''):
        self.true = true
        self.false = false
        self.items = items
        self.iterable = iterable
    def render(self, context):
        output = []
        if iterable:
            for i in iterable:
                var_list = [(item, i[self.items.index(item)]) for item in self.items]
                new_context = dict(list(context.items()) + var_list)
                output.append(self.true.render(new_context))
            output = ''.join(output)
        else:
            output = self.false.render(context)
        # return ''.join(self.true.render(dict(list(context.items())+[(item, i[self.items.index(item)])]) for item in self.items]) for i in iterable) if iterable else self.false.render(context)
        return output

class CommentNode(Node):
    def __init__(self, comment):
        self.comment = comment
    def render(self, context):
        return ''

class LetNode(Node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    def render(self, context):
        context[self.var] = eval(self.expr)

def create(content, context):
    
    def parse(content, node_list = None):
        content = list(content)
        if not node_list: node_list = []
        while content:
            
            if ''.join(content).startswith('{{'): # PythonNode
                for _ in range(2): content.pop(0)
                node = PythonNode(content.pop(0))
                while not ''.join(content).startswith('}}'):
                    node.code += content.pop(0)
                for _ in range(2): content.pop(0)
                node.code = node.code.strip()
                node_list.append(node)

            elif ''.join(content).startswith('{%'): # if or include
                for _ in range(3): content.pop(0)
                
                if ''.join(content).startswith('if') : # IfNode
                    for _ in range(3): content.pop(0)
                    node = IfNode(content.pop(0), '')
                    while not ''.join(content).startswith('%}'):
                        node.predicate += content.pop(0)
                    for _ in range(2): content.pop(0)
                    node.predicate = node.predicate.strip()
                    true_content = []
                    stack = 0
                    while stack >= 0:
                        true_content.append(content.pop(0))
                        if ''.join(content).startswith('{% end if %}'): stack -= 1
                        if ''.join(content).startswith('{% if'): stack += 1
                    for _ in range(len('{% end if %}')): content.pop(0)
                    node.true = GroupNode(parse(true_content))
                    node_list.append(node)

                elif ''.join(content).startswith('include'): # IncludeNode
                    for _ in range(8): content.pop(0)
                    node = IncludeNode('')
                    while not ''.join(content).startswith('%}'):
                        node.path += content.pop(0)
                    for _ in range(2): content.pop(0)
                    node.path = node.path.strip()
                    node_list.append(node)
                    
            else: # TextNode
                node = TextNode('')
                while content and not (''.join(content).startswith('{%') or ''.join(content).startswith('{{')):
                    node.content += content.pop(0)
                node_list.append(node)

        return node_list

    raw = parse(content)
    output = ''
    for part in raw:
        output += part.render(context)
    return output

if __name__ == '__main__':
    f = ''.join(open('template_sample.html').readlines())
    context = {'f_name': 'john smith',
               'f_age': '100',
               'f_gender': 'M',
               'person_name':'asem wardak'}
    output_file = open('output.html', 'w')
    output_file.write(create(f, context))
    output_file.close()
    print(create(f, context))
