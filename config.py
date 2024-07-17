# GRAPH_TEMPLATE = {
#     'desc': {
#         'slots': ['disease'],
#         'question': '什么叫%disease%? / %disease%是一种什么病？',
#         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.desc AS RES",
#         'answer': '【%disease%】的定义：%RES%',
#     },
#     'cause': {
#         'slots': ['disease'],
#         'question': '%disease%一般是由什么引起的？/ 什么会导致%disease%？',
#         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.cause AS RES",
#         'answer': '【%disease%】的病因：%RES%',
#     },
#     'disease_symptom': {
#         'slots': ['disease'],
#         'question': '%disease%会有哪些症状？/ %disease%有哪些临床表现？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_SYMPTOM]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%disease%】的症状：%RES%',
#     },
#     'symptom': {
#         'slots': ['symptom'],
#         'question': '%symptom%可能是得了什么病？',
#         'cypher': "MATCH (n)-[:DISEASE_SYMPTOM]->(m:Symptom) WHERE m.name='%symptom%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(n.name) | s + '、' + x), 1) AS RES",
#         'answer': '可能出现【%symptom%】症状的疾病：%RES%',
#     },
#     'cure_way': {
#         'slots': ['disease'],
#         'question': '%disease%吃什么药好得快？/ %disease%怎么治？',
#         'cypher': '''
#             MATCH (n:Disease)-[:DISEASE_CUREWAY]->(m1),
#                 (n:Disease)-[:DISEASE_DRUG]->(m2),
#                 (n:Disease)-[:DISEASE_DO_EAT]->(m3)
#             WHERE n.name = '%disease%'
#             WITH COLLECT(DISTINCT m1.name) AS m1Names, 
#                 COLLECT(DISTINCT m2.name) AS m2Names,
#                 COLLECT(DISTINCT m3.name) AS m3Names
#             RETURN SUBSTRING(REDUCE(s = '', x IN m1Names | s + '、' + x), 1) AS RES1,
#                 SUBSTRING(REDUCE(s = '', x IN m2Names | s + '、' + x), 1) AS RES2,
#                 SUBSTRING(REDUCE(s = '', x IN m3Names | s + '、' + x), 1) AS RES3
#             ''',
#         'answer': '【%disease%】的治疗方法：%RES1%。\n可用药物：%RES2%。\n推荐食物：%RES3%',
#     },
#     'cure_department': {
#         'slots': ['disease'],
#         'question': '得了%disease%去医院挂什么科室的号？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_DEPARTMENT]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%disease%】的就诊科室：%RES%',
#     },
#     'prevent': {
#         'slots': ['disease'],
#         'question': '%disease%要怎么预防？',
#         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.prevent AS RES",
#         'answer': '【%disease%】的预防方法：%RES%',
#     },
#     'not_eat': {
#         'slots': ['disease'],
#         'question': '%disease%换着有什么禁忌？/ %disease%不能吃什么？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_NOT_EAT]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%disease%】的患者不能吃的食物：%RES%',
#     },
#     'check': {
#         'slots': ['disease'],
#         'question': '%disease%要做哪些检查？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_CHECK]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%disease%】的检查项目：%RES%',
#     },
#     'cured_prob': {
#         'slots': ['disease'],
#         'question': '%disease%能治好吗？/ %disease%治好的几率有多大？',
#         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.cured_prob AS RES",
#         'answer': '【%disease%】的治愈率：%RES%',
#     },
#     'acompany': {
#         'slots': ['disease'],
#         'question': '%disease%的并发症有哪些？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_ACOMPANY]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%disease%】的并发症：%RES%',
#     },
#     'indications': {
#         'slots': ['drug'],
#         'question': '%drug%能治那些病？',
#         'cypher': "MATCH (n:Disease)-[:DISEASE_DRUG]->(m:Drug) WHERE m.name='%drug%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(n.name) | s + '、' + x), 1) AS RES",
#         'answer': '【%drug%】能治疗的疾病有：%RES%',
#     },
# }

CROP_GRAPH_TEMPLATE = {
    'crop_desc': {
    'slots': ['crop'],
    'question': '什么是%crop%？ / %crop%是什么植物？',
    'cypher': "MATCH (n:Crop) WHERE n.title='%crop%' RETURN n.detail AS RES",
    'answer': '【%crop%】的定义：%RES%',
    },
    'crop_classification': {
        'slots': ['crop'],
        'question': '%crop%属于什么类别？/ %crop%属于什么科？',
        'cypher': "MATCH (n:Crop)-[r:Crop2HudongItem {type: 'parent taxon'}]->(m) WHERE n.title = '%crop%' RETURN m.title AS RES",
        'answer': '【%crop%】的分类：%RES%',
    },
    'crop_fruit': {
        'slots': ['crop'],
        'question': '%crop%结什么样的果实？',
        'cypher': "MATCH (n:Crop)-[r:Crop2HudongItem {type: 'has fruit type'}]->(m) WHERE n.title = '%crop%' RETURN m.title AS RES",
        'answer': '【%crop%】的果实：%RES%',
    },
}