import json
import math
import copy

# def check_not_exist_link(data):
#     links = data['links']
#     nodes = data['nodes']

#     # Check existing link's id in nodes.
#     links_ids = []
#     not_exist_links = []
#     for l in links:
#         links_ids.append(l['id'])
#         is_exist = False
#         for n in nodes:
#             if 'inputs' in n:
#                 for ip in n['inputs']:
#                     if 'link' in ip and ip['link'] == l['id']:
#                         is_exist = True
#                         break
#             if 'outputs' in n:
#                 for ip in n['outputs']:
#                     if 'links' in ip and ip['links'] is not None and l['id'] in ip['links']:
#                         is_exist = True
#                         break
#         if not is_exist:
#             not_exist_links.append(l['id'])

#     # if not_exist_links:
#     #     print(f"Exist Invalid link -> {not_exist_links}")
#     #     exit(1)

#     return not_exist_links

def check_link(data):
    links = data['links']
    nodes = data['nodes']

    links_ids = []
    not_couple_links = []
    not_exist_links = []
    duplicated_links = []
    for l in links:
        links_ids.append(l['id'])
        inputs_exist = False
        ouputs_exist = False
        for n in nodes:
            if 'inputs' in n:
                for ip in n['inputs']:
                    if 'link' in ip and ip['link'] == l['id']:
                        if inputs_exist:
                            duplicated_links.append(l['id'])
                        inputs_exist = True

            if 'outputs' in n:
                for ip in n['outputs']:
                    if 'links' in ip and ip['links'] is not None and l['id'] in ip['links']:
                        if ouputs_exist:
                            duplicated_links.append(l['id'])
                        ouputs_exist = True

        if not inputs_exist and not ouputs_exist:
            not_exist_links.append(l['id'])
        elif not inputs_exist or not ouputs_exist:
            not_couple_links.append(l['id'])

    # if not_exist_links:
    #     print(f"Exist Invalid link -> {not_exist_links}")
    #     exit(1)

    return not_exist_links, not_couple_links, duplicated_links


def find_item(items, item_id):
    for i in items:
        if i['id'] == item_id:
            return i
    return None


def check_tasks(data):
    print(f"A number of tasks : {len(data['tasks'])}")
    print(f"A number of nodes : {len(data['nodes'])}")
    print(f"A number of links : {len(data['links'])}")

    t_ids = []
    for t in data['tasks']:
        if t['id'] in t_ids:
            print(f"Duplicated task ID!! : {t['id']}")
        else:
            t_ids.append(t['id'])

    t_ids = []
    for t in data['nodes']:
        if t['id'] in t_ids:
            print(f"Duplicated node ID!! : {t['id']}")
        else:
            t_ids.append(t['id'])

    t_ids = []
    for t in data['links']:
        if t['id'] in t_ids:
            print(f"Duplicated link ID!! : {t['id']}")
        else:
            t_ids.append(t['id'])


def remove_links(data, remove_list):
    for link_id in remove_list:
        ln = find_item(data['links'], link_id)
        data['links'].remove(ln)


# 가장 오른쪽의 좌표를 가져온다.
def outline_right_for_tasks(tasks):
    outline = -10000.0
    for t in tasks:
        x, y, w, h = t['ui_setting']['bounding']
        r = x + w
        if outline < r:
            outline = r
    return outline


# 가장 왼쪽의 좌표를 가져온다.
def outline_left_for_tasks(tasks):
    outline = 10000.0
    for t in tasks:
        x, y, w, h = t['ui_setting']['bounding']
        l = x
        if outline > l:
            outline = l
    return outline


# 가장 아래의 좌표를 가져온다.
def outline_bottom_for_tasks(tasks):
    outline = -10000.0
    for t in tasks:
        x, y, w, h = t['ui_setting']['bounding']
        b = y + h
        if outline < b:
            outline = b
    return outline


# 가장 위의 좌표를 가져온다.
def outline_top_for_tasks(tasks):
    outline = 10000.0
    for t in tasks:
        x, y, w, h = t['ui_setting']['bounding']
        t = y
        if outline > t:
            outline = t
    return outline


# Task 전체의 너비를 가져온다.
def outline_width_for_tasks(tasks):
    l = outline_left_for_tasks(tasks)
    r = outline_right_for_tasks(tasks)
    return r - l


# Task 전체의 높이를 가져온다.
def outline_height_for_tasks(tasks):
    t = outline_top_for_tasks(tasks)
    b = outline_bottom_for_tasks(tasks)
    return b - t


def get_new_id(items):
    last_id = -1
    for i in items:
        cur_id = i['id']
        if last_id < cur_id:
            last_id = cur_id
    return last_id + 1


def copy_all(data, count):
    COL_COUNT = 2
    MARGIN = 0.1

    tasks = data['tasks']
    nodes = data['nodes']
    links = data['links']

    task_id_offset = get_new_id(tasks)
    node_id_offset = get_new_id(nodes)
    link_id_offset = get_new_id(links)

    r_offset = outline_right_for_tasks(tasks) + MARGIN
    b_offset = outline_bottom_for_tasks(tasks) + MARGIN

    new_task_list = []
    new_nodes_list = []
    new_links_list = []

    bottom_offset = None

    for idx in range(1, count):
        print(idx)
        print(f'tasks count : {len(tasks)}')
        right_offset = r_offset
        col_num = int(idx % COL_COUNT)
        row_num = math.floor(idx / COL_COUNT)

        right_offset = col_num * r_offset
        bottom_offset = row_num * b_offset
        print(f'right offset : {right_offset}')
        print(f'bottom offset : {bottom_offset}')

        # for i in range(idx - 2 % COL_COUNT):

        for t in tasks:
            task_nodes = [n for n in nodes if n['task_id'] == t['id']]
            task_links = []
            for l in links:
                for n in task_nodes:
                     if l['origin_id'] == n['id'] or l['target_id'] == n['id']:
                         task_links.append(l)
                         break

            # print(f'node count : {len(task_nodes)}')
            # print(f'link count : {len(task_links)}')


            task_id_offset, node_id_offset, link_id_offset, new_task, new_nodes, new_links = \
                copy_task(idx, task_id_offset, node_id_offset, link_id_offset,
                          t, task_nodes, task_links, right_offset, bottom_offset)
            # print(new_task)
            new_task_list.append(new_task)
            new_nodes_list.append(new_nodes)
            new_links_list.append(new_links)

    data['tasks'].extend(new_task_list)
    for n in new_nodes_list:
        data['nodes'].extend(n)
    for n in new_links_list:
        data['links'].extend(n)

    return data


def copy_task(tag, task_id_offset, node_id_offset, link_id_offset, ori_task, nodes, links, r_offset, b_offset):
    dest_task = copy.deepcopy(ori_task)
    # print(f'node count : {len(nodes)}')
    # print(f'link count : {len(links)}')
    dest_nodes = copy.deepcopy(nodes)
    dest_links = copy.deepcopy(links)

    # new task title.
    new_task_title = f"{dest_task['title']}_{tag}"

    # Node and Link.

    # Make tuples with original id and target id for node.
    node_id_list = []
    for n in dest_nodes:
        ori_node_id = n['id']
        dest_node_id = node_id_offset
        node_id_list.append((ori_node_id, dest_node_id))
        node_id_offset += 1

    # Make tuples with original id and target id for link.
    link_id_list = []
    for n in dest_links:
        ori_link_id = n['id']
        dest_link_id = link_id_offset
        link_id_list.append((ori_link_id, dest_link_id))
        link_id_offset += 1

    def replace_id(items, ori):
        for i in items:
            if i[0] == ori:
                return i[1]
        return None

    for n in dest_nodes:
        # Change id.
        n['id'] = replace_id(node_id_list, n['id'])
        if 'inputs' in n and n['inputs'] is not None:
            for i in range(len(n['inputs'])):
                # print(n['inputs'][i])
                if 'link' in n['inputs'][i] and n['inputs'][i]['link'] is not None:
                    n['inputs'][i]['link'] = replace_id(link_id_list, n['inputs'][i]['link'])

        if 'outputs' in n and n['outputs'] is not None:
            for i in range(len(n['outputs'])):
                # print(n['outputs'][i])
                if 'links' in n['outputs'][i] and n['outputs'][i]['links'] is not None:
                    for k in range(len(n['outputs'][i]['links'])):
                        n['outputs'][i]['links'][k] = replace_id(link_id_list, n['outputs'][i]['links'][k])

        n['task_id'] = task_id_offset

        # Change ui.
        n['ui_setting']['pos'][0] += r_offset
        n['ui_setting']['pos'][1] += b_offset

        # Additional!
        change_prop_names_type1 = ['input_query', 'signal_name', 'output_query']
        change_prop_names_type2 = ['url']

        if n['type'] == 'signal/async_signal':
            for prop in n['properties']:
                if prop['name'] in change_prop_names_type1:
                    if 'value' not in prop or prop['value'] is None or not prop['value'].strip():
                        continue
                    tokens = prop['value'].split('::')
                    tokens[-2] = f'{tokens[-2]}_{tag}'
                    prop['value'] = '::'.join(tokens)
                if prop['name'] in change_prop_names_type2:
                    tokens = prop['value'].split('.')
                    tokens[-2] = f'{tokens[-2]}_{tag}'
                    prop['value'] = '.'.join(tokens)

        change_types = ['posod/posod_fall_down_filter', 'posod/posod_fall_filter', 'posod/posod_helmet_filter', 'posod/posod_fire_filter', 'posod/posod_intrude_filter']
        change_prop_names_type1 = ['bucket_name']
        if n['type'] in change_types:
            for prop in n['properties']:
                if prop['name'] in change_prop_names_type1:
                    if 'value' not in prop or prop['value'] is None or not prop['value'].strip():
                        continue
                    prop['value'] = f"{prop['value']}-{tag}"

    for l in dest_links:
        l['id'] = replace_id(link_id_list, l['id'])
        l['origin_id'] = replace_id(node_id_list, l['origin_id'])
        l['target_id'] = replace_id(node_id_list, l['target_id'])

    # Task.

    # Change id.
    dest_task['id'] = task_id_offset

    # Change title.
    dest_task['title'] = new_task_title

    # Change bounding.
    dest_task_bounding = dest_task['ui_setting']['bounding']
    dest_task_bounding[0] += r_offset
    dest_task_bounding[1] += b_offset

    # Add Nodes.
    dest_task['nodes'] = [ n['id'] for n in dest_nodes if n['task_id'] == task_id_offset ]


    # print(f'dest_links count : {len(dest_links)}')

    return (task_id_offset + 1), node_id_offset, link_id_offset, dest_task, dest_nodes, dest_links


if __name__ == "__main__":
    with open('/Users/nasoo/Downloads/2ch.json', 'r') as f:
        data = json.load(f)
    not_exist_links, not_couple_links, duplicated_links = check_link(data)
    print(f"Exist Invalid link -> {not_exist_links}")
    print(f"not Couple link -> {not_couple_links}")
    print(f"Duplicated link -> {duplicated_links}")

    remove_links(data, not_exist_links)


    not_exist_links, not_couple_links, duplicated_links = check_link(data)
    print(f"Exist Invalid link -> {not_exist_links}")
    print(f"not Couple link -> {not_couple_links}")
    print(f"Duplicated link -> {duplicated_links}")

    data = copy_all(data, 8)

    with open('answertest14.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)

    check_tasks(data)
