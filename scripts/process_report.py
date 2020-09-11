# this file is used to process issue reports in order to obtain plain text.
# encoding=utf8 
import csv
import re
import collections

def run(description):
    is_code = False  # iscode
    is_comment = False # iscomment
    is_t = False  # istable
    content = None
    content_c = None

    content_comment = None
    mark = ''
    mark_comment = ''
 
    # parse markDown 
    descriptions = description.split('\n')
    for line in descriptions:
        line = line.lstrip()
        result, result_comment, result1, content_c, content, mark, content_comment, mark_comment = parse(line, is_code, is_comment, is_t, mark, mark_comment, content, content_c, content_comment)
        is_code = result
        is_comment = result_comment
        is_t = result1
        content = content
        content_c = content_c
        mark = mark
        content_comment = content_comment
        mark_comment = mark_comment

 
 
def parse(input_, is_code, is_comment, is_t, mark='', mark_comment = '', content=None, content_c=None, content_comment=None):
    # parse code snipets， mark is the tag of code tyype
    is_c, content_c, mark = test_code(input_, is_code, mark, content_c=content_c)
    # parse code snipets， mark is the tag of code tyype
    if not is_c:
        is_comment, content_comment, mark_comment = test_comment(input_, is_comment, mark_comment, content_comment=content_comment)
    
    
    # parse image
    if not is_c and not is_comment:
        res = test_link(input_)
        if not res:
            # parse title
            res1 = test_header(input_)
            if not res1:
                # parse table
                is_t, content = test_table(input_, is_t, content=content)
                if not is_t:
                    res3 = test_list(input_)
                    if not res3:
                        test_normal(input_)
    pattern_end = re.compile(r'(.*)-->')
    a_end = pattern_end.match(input_)
    if a_end:
        is_comment = False

    return is_c, is_comment, is_t, content_c, content, mark, content_comment, mark_comment
 
 
# match title
def test_header(input_):
    # analyze title tag
    global body_content
    title_rank = 0
    for i in range(6, 0, -1):
        if input_[:i] == '#' * i:
            title_rank = i
            break
    else:
        return 0
    input_ = input_.replace('**', '')
    header = input_[title_rank:]
    body_content += (input_[title_rank:].lstrip() + '\n')
    return 1
 
 
def test_normal(input_):
    # match balnk line
    global body_content
    input_bold = ''
    if input_ == '\n' or input_ == '`':
    	#body_content += input_
        return
    if '``' in input_:
        pass
    else:
        test_pattern = re.compile(r'(.*)\*\*(.*)\*\*(.*)')
        test_match = test_pattern.match(input_)
        pattern = re.compile(r'(.*?)\*\*(.*?)\*\*(.*?)')
        match = pattern.finditer(input_)
 
        if match:
            try:
                for i in match:
                    a = i.group(1)
                    b = i.group(2)
                    c = i.group(3)
                    input_bold += a  + b + c
                # split joint
                input_bold += test_match.group(3)
                input_ = input_bold
            except:
                pass
        input_last = input_.replace('	', '')
        body_content += (input_last.lstrip() + '\n')
 
 
# match code
def test_code(input_, is_code, mark, content_c=None):
    global num_code
    if not content_c:
        content_c = []
    pattern = re.compile(r'`(.*)') 
    #print input_
    a = pattern.match(input_)
    if a or is_code:
        if a and is_code:
            is_code = False
            # is code
            num_code += 1
            content_c = []
        else:
            is_code = True
            try:
                mark = a.group(1)
            except:
                pass
 
            if not a:
                content_c.append(input_)
        #print input_, is_code, content_c, mark
 
        return is_code, content_c, mark
    return is_code, content_c, mark

# match comment
def test_comment(input_, is_comment, mark_comment, content_comment=None):
    global num_comment
    if not content_comment:
        content_comment = []
    pattern = re.compile(r'<!--(.*)')
    pattern_end = re.compile(r'(.*)-->')
    a = pattern.match(input_)
    a_end = pattern_end.match(input_)
    if a or is_comment or a_end:
        if a_end and is_comment:
            #print('&&&&', input_)
            #is_comment = False
            num_comment += 1
            content_comment = []
        elif a and a_end:
            num_comment += 1
            content_comment = []
            is_comment = True
        elif a and not is_comment:
            is_comment = True
            try:
                mark_comment = a.group(1)
            except:
                pass
 
        elif not a and is_comment:
                content_comment.append(input_)
        #print input_, is_comment, content_comment, mark_comment 
 
        return is_comment, content_comment, mark_comment
    return is_comment, content_comment, mark_comment
 
 
def all_same(lst, sym):
    return not lst or sym * len(lst) == lst
 
 
def test_list(input_):
    global body_content
    if len(input_) > 2 and input_[0].isdigit() and input_[1] == '.':
        result = input_[2:].lstrip()
        body_content += (result + '\n')
        return 1
 
    if len(input_) > 2 and all_same(input_[:-1], '-') and input_[-1] == '\n':
        body_content += (input_ + '\n')
        return 1
 
    if input_ != "" and input_[0] in ['+', '-']:
        result = input_[1:]
        body_content += (result + '\n')
        return 1
    return 0
 
 
def test_table(input_, is_t, content=None):
    global num_table
    if not content:
        content = collections.defaultdict(list)
    pattern = re.compile(r'^(.*)\|(.+)$')
    match = pattern.match(input_)
    if match:
        l = input_.split('|')
        l[-1] = l[-1][:-1]
        if l[0] == '':
            l.pop(0)
        if l[-1] == '':
            l.pop(-1)
        if l and '--' in l[0]:
            return is_t, content
        if not is_t:
            content['th'].append(l)
        else:
            content['td'].append(l)
        is_t = True
    else:
        is_t = False
 
        if not is_t and content:
            num_table += 1
            content = None
    return is_t, content
 
 
def test_link(s):
    global num_image
    global num_url
    pattern = re.compile(r'(.*)\[(.*?)\]\((.*?)\)')
    match = pattern.finditer(s)
    for a in match:
        if a:
            text, url = a.group(1, 2)
            num_url += 1
            return 1
 
    pattern = re.compile(r'^!\[(.*)\]\((.*)\)')
    match = pattern.finditer(s)
    for a in match:
        if a:
            text, url = a.group(1, 2)
            num_image += 1
            return 1
 
    return 0


if __name__=="__main__":
    csv.field_size_limit(500 * 1024 * 1024) 
    file1 = open('issue_data.csv')
    csv_reader = csv.reader(file1)
    header = next(csv_reader)
    file2 = open('new_issue_data.csv', 'wb')
    csv_writer = csv.writer(file2)
    csv_writer.writerow(['id', 'title', 'body_content', 'num_url', 'num_image', 'num_code', 'num_comment', 'num_table', 'whether_sovled_by_newcomer'])
    for row in csv_reader:
        id = row[0]
        title = row[1]
        description = row[2]
        whether_sovled_by_newcomer = row[3]
        body_content = '' 
        num_url = 0
        num_image = 0
        num_code = 0
        num_comment = 0
        num_table = 0
        run(description)
        csv_writer.writerow([id, title, body_content, num_url, num_image, num_code, num_comment, num_table, whether_sovled_by_newcomer])
    file1.close()
    file2.close()