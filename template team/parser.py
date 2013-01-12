from template_language import *
f = list(''.join(open('template_sample.html').readlines()))

def parse(content, node_list = None):
    # do stuff
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
                for _ in range(3): content.pop(0)#
                node = IfNode(content.pop(0), '')
                while not ''.join(content).startswith('%}'):
                    node.predicate += content.pop(0)
                for _ in range(2): content.pop(0)
                node.predicate = node.predicate.strip()
                true_content = []
                while not ''.join(content).startswith('{% end if %}'):
                    true_content.append(content.pop(0))
                for _ in range(len('{% end if %}')): content.pop(0)
                node.true = GroupNode(parse(true_content))
                node_list.append(node)
                
        else: # TextNode
            node = TextNode('')
            while content and not (''.join(content).startswith('{%') or ''.join(content).startswith('{{')):
                node.content += content.pop(0)
            node_list.append(node)

    return node_list
            
a = parse(f)
context = {'f_name': 'asem wardak', 'f_age': '15', 'f_gender': 'M', 'person_name':'lol'}
for b in a:
    print(b.render(context))
