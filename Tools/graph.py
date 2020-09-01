# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/8/3 16:00
# IDE：PyCharm

import pandas as pd

# 构建图的节点和关系
def construct_graph_node_relation(inside_data, inside_nodes):
    temp_relation = pd.DataFrame(columns=['left_node', 'right_node', 'right_type'])
    temp_node = pd.DataFrame(columns=['node_key', 'node_type'])

    # 添加uuid节点
    temp_node = add_node(temp_node, inside_data, 'dw_graph_cash_loan_event.event_uuid', 'uuid')

    # 添加uuid-uid的节点和关系
    for column, node_type in inside_nodes:
        print('正在添加' + str(node_type) + '的节点和关系')
        temp_node = add_node(temp_node, inside_data, column, node_type)
        temp_relation = add_relation(temp_relation, inside_data, column, node_type)
    temp_node.reset_index(drop=True, inplace=True)
    temp_relation.reset_index(drop=True, inplace=True)
    return temp_node, temp_relation


data = pd.read_excel('Data/files/2020_8.xlsx', header=0)
nodes = [('dw_graph_cash_loan_event.uid', 'uid'),
         ('dw_graph_cash_loan_event.device_id', 'device'),
         ('dw_graph_cash_loan_event.v_plate_no', 'plate'),
         ('dw_graph_cash_loan_event.id_card_no', 'id'),
         ('dw_graph_cash_loan_event.pdl_card_mobile', 'mobile'),
         ('dw_graph_cash_loan_event.d_identity_no', 'driver')]
node, relation = construct_graph_node_relation(data, nodes)


# 根据节点和关系的数据，给每个连通图分配图ID
def construct_graph_id():
    global node, relation
    node['graph_id'], relation['graph_id'] = [0] * len(node), [0] * len(relation)

    for index, row in enumerate(node.itertuples()):
        graph_id, node_type, node_key = getattr(row, 'graph_id'), getattr(row, 'node_type'), getattr(row, 'node_key')
        if graph_id > 0:
            continue
        current_graph_id = max(node['graph_id'].values) + 1
        print('正在更新类型为' + node_type + '且主键为' + node_key + '的节点信息')
        if node_type == 'uuid':
            update_left_key(node_key, current_graph_id)
        else:
            update_right_key(node_key, node_type, current_graph_id)


# 进行连通图的划分
construct_graph_id()


# 更新节点为node_key和关系左节点为node_key的graph_id
def update_left_key(node_key, current_graph_id):
    global node, relation
    right_key_to_update = []

    # 更新节点为node_key且类型为uuid的节点的graph_id
    list_node_index = (node[(node['node_key'] == node_key) & (node['graph_id'] == 0)
                            & (node['node_type'] == 'uuid')].index.tolist())
    if len(list_node_index) == 0:
        return

    print('---正在更新主键为' + node_key + '的左节点信息')
    for node_index in list_node_index:
        node.loc[node_index, 'graph_id'] = current_graph_id

    # 更新左节点为node_key的关系的graph_id
    for relation_index in relation[(relation['left_node'] == node_key) & (relation['graph_id'] == 0)].index.tolist():
        relation.loc[relation_index, 'graph_id'] = current_graph_id
        right_key_to_update.append((relation.loc[relation_index, 'right_node'],
                                    relation.loc[relation_index, 'right_type']))

    # 更新左节点为node_key的右节点的节点graph_id及其关联的关系的graph_id
    for right_node, right_type in right_key_to_update:
        update_right_key(right_node, right_type, current_graph_id)


# 更新节点为node_key且类型为node_type的graph_id及其关系的graph_id
def update_right_key(node_key, node_type, current_graph_id):
    global node, relation
    left_key_to_update = []

    # 更新节点为node_key且类型为node_type的节点的graph_id
    list_node_index = (node[(node['node_key'] == node_key) & (node['graph_id'] == 0)
                            & (node['node_type'] == node_type)].index.tolist())
    if len(list_node_index) == 0:
        return

    print('---正在更新类型为' + node_type + '且主键为' + node_key + '的右节点信息')

    for node_index in list_node_index:
        node.loc[node_index, 'graph_id'] = current_graph_id

    # 更新左节点为node_key的关系的graph_id
    for relation_index in relation[(relation['right_node'] == node_key) & (relation['graph_id'] == 0)
                                   & (relation['right_type'] == node_type)].index.tolist():
        relation.loc[relation_index, 'graph_id'] = current_graph_id
        left_key_to_update.append(relation.loc[relation_index, 'left_node'])

    # 更新左节点为node_key的右节点的节点graph_id及其关联的关系的graph_id
    for left_node in left_key_to_update:
        update_left_key(left_node, current_graph_id)


# 添加关系网络中的节点
def add_node(inside_node, inside_data, column, node_type):
    # 只添加不在node中的元素
    added_node_value = inside_node[inside_node['node_type'] == node_type]['node_key'].values
    new_node_value = list(filter(lambda x: False if x in list(added_node_value) else True,
                                 list(set(inside_data[column].values))))
    # 排除异常值
    new_node_value = list(filter(lambda x: False if x in ['', '_unknown'] else True,
                                 new_node_value))
    return inside_node.append(pd.DataFrame({
        'node_key': new_node_value,
        'node_type': [node_type] * len(new_node_value)
    }))


# 添加关系网络中的关系
def add_relation(inside_relation, inside_data, column, node_type, key_column='dw_graph_cash_loan_event.event_uuid'):
    # 排除为空或_unknown的节点
    new_relation = inside_data[[key_column, column]].copy()
    new_relation = new_relation[new_relation.apply(
        lambda x: False if ((x[column] in ['', '_unknown']) or (x[key_column] in ['', '_unknown']))
        else True, axis=1)].copy()

    # 排除已添加到关系的节点
    if len(inside_relation) > 0:
        added_relation_value = list(inside_relation[inside_relation['right_type'] == node_type].apply(
            lambda x: str(str(x['left_node']) + str(x['right_node'])), axis=1))
        new_relation['Result'] = new_relation.apply(
            lambda x: str(x[key_column]) + str(x[column]), axis=1)
        new_relation = new_relation[
            list(new_relation.apply(lambda x: False if x['Result'] in added_relation_value else True, axis=1))
        ]

    return inside_relation.append(pd.DataFrame({
        'left_node': new_relation[key_column].values,
        'right_node': new_relation[column].values,
        'right_type': [node_type] * len(new_relation),
    }))
