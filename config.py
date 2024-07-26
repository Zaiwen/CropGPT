
CROP_GRAPH_TEMPLATE = {
     'desc': {
         'slots': ['disease'],
         'question': '什么叫%disease%? / %disease%是一种什么病？',
         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.desc AS RES",
         'answer': '【%disease%】的定义：%RES%',
     },
     'cause': {
         'slots': ['disease'],
         'question': '%disease%一般是由什么引起的？/ 什么会导致%disease%？',
         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.cause AS RES",
         'answer': '【%disease%】的病因：%RES%',
     },
     'disease_symptom': {
         'slots': ['disease'],
         'question': '%disease%会有哪些症状？/ %disease%有哪些临床表现？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_SYMPTOM]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
         'answer': '【%disease%】的症状：%RES%',
     },
     'symptom': {
         'slots': ['symptom'],
         'question': '%symptom%可能是得了什么病？',
         'cypher': "MATCH (n)-[:DISEASE_SYMPTOM]->(m:Symptom) WHERE m.name='%symptom%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(n.name) | s + '、' + x), 1) AS RES",
         'answer': '可能出现【%symptom%】症状的疾病：%RES%',
     },
     'cure_way': {
         'slots': ['disease'],
         'question': '%disease%吃什么药好得快？/ %disease%怎么治？',
         'cypher': '''
             MATCH (n:Disease)-[:DISEASE_CUREWAY]->(m1),
                 (n:Disease)-[:DISEASE_DRUG]->(m2),
                 (n:Disease)-[:DISEASE_DO_EAT]->(m3)
             WHERE n.name = '%disease%'
             WITH COLLECT(DISTINCT m1.name) AS m1Names, 
                 COLLECT(DISTINCT m2.name) AS m2Names,
                 COLLECT(DISTINCT m3.name) AS m3Names
             RETURN SUBSTRING(REDUCE(s = '', x IN m1Names | s + '、' + x), 1) AS RES1,
                 SUBSTRING(REDUCE(s = '', x IN m2Names | s + '、' + x), 1) AS RES2,
                 SUBSTRING(REDUCE(s = '', x IN m3Names | s + '、' + x), 1) AS RES3
             ''',
         'answer': '【%disease%】的治疗方法：%RES1%。\n可用药物：%RES2%。\n推荐食物：%RES3%',
     },
     'cure_department': {
         'slots': ['disease'],
         'question': '得了%disease%去医院挂什么科室的号？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_DEPARTMENT]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
         'answer': '【%disease%】的就诊科室：%RES%',
     },
     'prevent': {
         'slots': ['disease'],
         'question': '%disease%要怎么预防？',
         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.prevent AS RES",
         'answer': '【%disease%】的预防方法：%RES%',
     },
     'not_eat': {
         'slots': ['disease'],
         'question': '%disease%换着有什么禁忌？/ %disease%不能吃什么？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_NOT_EAT]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
         'answer': '【%disease%】的患者不能吃的食物：%RES%',
     },
     'check': {
         'slots': ['disease'],
         'question': '%disease%要做哪些检查？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_CHECK]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
         'answer': '【%disease%】的检查项目：%RES%',
     },
     'cured_prob': {
         'slots': ['disease'],
         'question': '%disease%能治好吗？/ %disease%治好的几率有多大？',
         'cypher': "MATCH (n:Disease) WHERE n.name='%disease%' RETURN n.cured_prob AS RES",
         'answer': '【%disease%】的治愈率：%RES%',
     },
     'acompany': {
         'slots': ['disease'],
         'question': '%disease%的并发症有哪些？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_ACOMPANY]->(m) WHERE n.name='%disease%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(m.name) | s + '、' + x), 1) AS RES",
         'answer': '【%disease%】的并发症：%RES%',
     },
     'indications': {
         'slots': ['drug'],
         'question': '%drug%能治那些病？',
         'cypher': "MATCH (n:Disease)-[:DISEASE_DRUG]->(m:Drug) WHERE m.name='%drug%' RETURN SUBSTRING(REDUCE(s = '', x IN COLLECT(n.name) | s + '、' + x), 1) AS RES",
         'answer': '【%drug%】能治疗的疾病有：%RES%',
     },
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
    'crop_period': {
        'slots': ['crop'],
        'question': '%crop%品种的生育期是多久？ / %crop%的生育期为？',
        'cypher': "match (n:品种) where n.name='%crop%' return n.生育期 as RES",
        'answer': '【%crop%】的生育期为%RES%',
    },
    'crop_characteristic': {
        'slots': ['crop'],
        'question': '为我介绍%crop%品种的特征特性？ / %crop%的特征特性为？',
        'cypher': "MATCH (n:品种) WHERE n.name = '黑糯305' RETURN n.name + '、株高：' + n.`株高` + '、生育期：' + n.`生育期` + '、穗位高：' + n.`穗位高` + '、百粒重：' + n.`百粒重` + '、穗长：' + n.`穗长` + '、叶片数：' + n.`叶片数` AS RES",
        'answer': '【%crop%】的特征特性：%RES%',
    },
    'crop_antidisease': {
        'slots': ['crop'],
        'question': '%crop%品种的对哪些疾病有抗性？ / %crop%的抗病类型为？',
        'cypher': "match (n:品种) where n.name='%crop%' return n.抗病类型 as RES",
        'answer': '【%crop%】的抗病类型为%RES%',
    },
    'crop_plant': {
        'slots': ['crop'],
        'question': '种植%crop%品种需要注意哪些地方？ / %crop%的栽培要点为？',
        'cypher': "match (n:品种)-[r:栽培要点]->(t1:`播种时间`),(n)-[r2:栽培要点]->(t2:播种密度) ,(n)-[r3:栽培要点]->(t3:种植地区),(n)-[r4:栽培要点]->(t4:管理方法)"
            " where n.name='先玉2036' return  t1.值 as re1,t2.值 as re2,t3.name as re3,t4.值 as re4",
        'answer': '【%crop%】的需要注意的地方有：%re1% + %re2% + %re3% + %re4%',
    },
    'crop_100weight': {
        'slots': ['crop'],
        'question': '%crop%品种的百粒重是多少？ / %crop%的百粒重为？',
        'cypher': "match (n:品种) where n.name='%crop%' return n.百粒重 as RES",
        'answer': '【%crop%】的百粒重为%RES%',
    },
    'crop_density': {
        'slots': ['crop'],
        'question': '%crop%适合的播种密度？ / %crop%的播种密度为？',
        'cypher': "match (n:品种)-[r:栽培要点]->(t:播种密度) where n.name='%crop%' return t.值 as RES",
        'answer': '【%crop%】的播种密度为%RES%',
    },
    'crop_time': {
        'slots': ['crop'],
        'question': '%crop%品种的播种时间是什么时候？收获时间是什么时候？ / %crop%的播种时间和收获时间分别为？',
        'cypher': "match (n:品种{name: '%crop%'})-[r1:栽培要点]->(t1:播种时间), (n)-[r2:栽培要点]->(t2:收获时间) return t1.值 as RES1, t2.值 as RES2",
        'answer': '【%crop%】的播种时间为%RES1%, 收获时间为%RES2%',
    },
    'location_maize': {
        'slots': ['province'],
        'question': '种植地区在%province%的玉米品种有哪些？ / %province%适合种植哪些品种的玉米？',
        'cypher': "MATCH (n:品种)-[r]->(t:种植地区) WHERE t.name CONTAINS '%province%' RETURN reduce(s = '', name IN collect(n.name) | s + name + '、') AS RES",
        'answer': '【%province%】适合种植的玉米有这些品种：%RES%',
    },
    'company_maize': {
        'slots': ['company'],
        'question': '%company%公司有哪些玉米品种？ / %company%选育过哪些玉米？',
        'cypher': "MATCH (n:品种)-[r]->(t:选育单位) WHERE t.name = '%company%' RETURN reduce(s = '', name IN collect(n.name) | s + name + '、') AS RES",
        'answer': '【%company%】选育的玉米有%RES%等等',
    },
    'crop_yield': {
        'slots': ['crop'],
        'question': '%cropy%种的产量预估能达到多少？ / %crop%品种的产量为？',
        'cypher': "MATCH (n:品种)-[r:`产量表现`]->(t:产量) WHERE n.name CONTAINS '%crop%' RETURN reduce(s = '', value IN collect(t.值) | s + value + '、') AS RES",
        'answer': '【%crop%】玉米预估产量能达到%RES%',
    },
    'maize_plant_time': {
        'slots': ['crop'],
        'question': '%crop%品种的播种时间是什么时候？',
        'cypher': 'match (n:品种{name:"%crop%"})-[:栽培要点]->(t:播种时间) return t.值 as RES',
        'answer': '【%crop%】的播种时间：%RES%',
    },
    'maize_harvest_time': {
        'slots': ['crop'],
        'question': '%crop%品种的收获时间是什么时候？',
        'cypher': 'match (n:品种{name:"%crop%"})-[:栽培要点]->(t:收获时间) return t.值 as RES',
        'answer': '【%crop%】的收获时间：%RES%',
    },
}