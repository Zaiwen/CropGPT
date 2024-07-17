import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from joblib import dump

# 数据加载函数
def load_data(filepath):
    return pd.read_excel(filepath)

# 文本预处理函数
def preprocess_text(text):
    text = text.lower()  # 转换为小写
    text = re.sub(r'\W', ' ', text)  # 移除非单词字符
    text = re.sub(r'\s+', ' ', text, flags=re.I)  # 替换多余的空格
    return text.strip()

# 主函数
def main():
    # 加载数据
    data = load_data(r'C:\Users\Roied\Desktop\新建文件夹\Code\code\project\data\分类器数据集.xlsx')
    
    # 文本预处理
    data['Processed Text'] = data['Input Description'].apply(preprocess_text)
    
    # 数据划分
    train_val_data, test_data = train_test_split(data, test_size=0.15, random_state=42, stratify=data['Model Label'])
    train_data, val_data = train_test_split(train_val_data, test_size=0.18, random_state=42, stratify=train_val_data['Model Label'])
    
    # TF-IDF向量化
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train = tfidf_vectorizer.fit_transform(train_data['Processed Text'])
    X_val = tfidf_vectorizer.transform(val_data['Processed Text'])
    X_test = tfidf_vectorizer.transform(test_data['Processed Text'])
    
    # 提取标签
    y_train = train_data['Model Label']
    y_val = val_data['Model Label']
    y_test = test_data['Model Label']
    
    
    # 初始化并训练逻辑回归模型
    log_reg = LogisticRegression(random_state=42, max_iter=1000)
    log_reg.fit(X_train, y_train)
    
    # 保存训练好的模型和TF-IDF向量化器
    dump(log_reg, 'trained_classifier.joblib')
    dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
    # 在验证集上进行预测
    y_val_pred = log_reg.predict(X_val)
    
    # 生成并打印分类报告
    print(classification_report(y_val, y_val_pred))


# 运行主函数
if __name__ == '__main__':
    main()
