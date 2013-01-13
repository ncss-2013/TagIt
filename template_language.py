from cgi import escape

class Node(object):
    def __init__(self): pass
    def _render(self): pass

class GroupNode(Node):
    def __init__(self, children = None):
        self.children = children if children else []
    def _render(self, context):
        return ''.join(str(child._render(context)) for child in self.children)

class TextNode(Node):
    def __init__(self, content = ''):
        self.content = content
    def _render(self, context):
        return self.content

class PythonNode(Node):
    def __init__(self, code = ''):
        self.code = code
    def _render(self, context):
        return eval(self.code, {}, context) if self.code else 'Not Implemented!'

class IfNode(Node):
    def __init__(self, predicate, true, false = ''):
        self.true = true
        self.false = false
        self.predicate = predicate
    def _render(self, context):
        return self.true._render(context) if eval(self.predicate, {}, context) else (self.false._render(context) if self.false else '')

class IncludeNode(Node):
    def __init__(self, path): #, var_dict = None):
        self.path = path
        # self.var_dict = var_dict if var_dict else {}
    def _render(self, context):
        # context.update(var_dict)
        return create(open(self.path).read(), context)

class ForNode(Node):
    def __init__(self, items, iterable, true, false = ''):
        self.true = true
        self.false = false
        self.items = items
        self.iterable = iterable
    def _render(self, context):
        output = []
        if self.iterable:
            print(self.iterable)
            print(self.items)
            for i in self.iterable._render(context):
                var_list = [(self.items[0], i)] # only supporting assigning 1 var in for statement
                # var_list = [(item, self.items[self.items.index(item)]) for item in self.items]
                print(self.items)
                new_context = dict(list(context.items()) + var_list)
                output.append(self.true._render(new_context))
            output = ''.join(output)
        else:
            output = self.false._render(context)
        # return ''.join(self.true._render(dict(list(context.items())+[(item, i[self.items.index(item)])]) for item in self.items]) for i in iterable) if iterable else self.false._render(context)
        return output

class CommentNode(Node):
    def __init__(self, comment):
        self.comment = comment
    def _render(self, context):
        return ''

class LetNode(Node):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    def _render(self, context):
        context[self.var] = eval(self.expr)

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
        elif ''.join(content).startswith('{%'):
            for _ in range(3): content.pop(0)
            if ''.join(content).startswith('if') : # IfNode
                for _ in range(3): content.pop(0)
                node = IfNode(content.pop(0), '')
                while not ''.join(content).startswith('%}'):
                    node.predicate += content.pop(0)
                for _ in range(2): content.pop(0)
                node.predicate = node.predicate.strip()
                true_content = []
                false_content = []
                stack_counter = 0
                while stack_counter >= 0:
                    true_content.append(content.pop(0))
                    if ''.join(content).startswith('{% end for %}'): stack_counter -= 1
                    if ''.join(content).startswith('{% for'): stack_counter += 1
                    if ''.join(content).startswith('{% end if %}'): stack_counter -= 1
                    if ''.join(content).startswith('{% if'): stack_counter += 1
                    if ''.join(content).startswith('{% else %}') and stack_counter == 0:
                        for _ in range(10): content.pop(0)
                        while stack_counter >= 0:
                            false_content.append(content.pop(0))
                            if ''.join(content).startswith('{% end if %}'): stack_counter -= 1
                            if ''.join(content).startswith('{% if'): stack_counter += 1
                for _ in range(len('{% end if %}')): content.pop(0)
                node.true = GroupNode(parse(true_content))
                if false_content: node.false = GroupNode(parse(false_content))
                node_list.append(node)
            elif ''.join(content).startswith('include'): # IncludeNode
                for _ in range(8): content.pop(0)
                node = IncludeNode('')
                while not ''.join(content).startswith('%}'):
                    node.path += content.pop(0)
                for _ in range(2): content.pop(0)
                node.path = node.path.strip()
                node_list.append(node)
            elif ''.join(content).startswith('for'): # ForNode
                for _ in range(4): content.pop(0)
                node = ForNode([], PythonNode(''), '')#items, iterable, true, false = '')
                items_str = ''
                iterable_str = ''
                while not ''.join(content).startswith('in'):
                    items_str += content.pop(0)
                node.items = items_str.split()
                for _ in range(3): content.pop(0)
                while not ''.join(content).startswith('%}'):
                    iterable_str += content.pop(0)
                node.iterable = PythonNode(iterable_str.strip())
                for _ in range(2): content.pop(0)
                true_content = []
                false_content = []
                stack_counter = 0
                while stack_counter >= 0:
                    true_content.append(content.pop(0))
                    if ''.join(content).startswith('{% end if %}'): stack_counter -= 1
                    if ''.join(content).startswith('{% if'): stack_counter += 1
                    if ''.join(content).startswith('{% end for %}'): stack_counter -= 1
                    if ''.join(content).startswith('{% for'): stack_counter += 1
                    if ''.join(content).startswith('{% else %}') and stack_counter == 0:
                        for _ in range(10): content.pop(0)
                        while stack_counter >= 0:
                            false_content.append(content.pop(0))
                            if ''.join(content).startswith('{% end for %}'): stack_counter -= 1
                            if ''.join(content).startswith('{% for'): stack_counter += 1
                for _ in range(len('{% end for %}')): content.pop(0)
                node.true = GroupNode(parse(true_content))
                if false_content: node.false = GroupNode(parse(false_content))
                node_list.append(node)
        else: # TextNode
            node = TextNode('')
            while content and not (''.join(content).startswith('{%') or ''.join(content).startswith('{{')):
                node.content += content.pop(0)
            node_list.append(node)
    return node_list

# Helper functions -----------
def create(content, context):
    raw = parse(content)
    output = ''
    for part in raw: output += str(part._render(context))
    return output
def render(f, c): return create(open(f, 'rU').read(), c)
# ----------------------------

if __name__ == '__main__':
    f = 'template/template_sample.html'
    context = {'f_name': 'john smith',
               'f_age': '100',
               'f_gender': 'F',
               'person_name':'asem wardak'}
    output_file = open('template/test_output.html', 'w')
    output_file.write(render(f, context))
    output_file.close()
    print(render(f, context))
