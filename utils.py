"""
工具函数模块
添加：预设场景生成、信息茧房模拟
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import random

# ========== 原有函数 ==========

def generate_dataset():
    """生成模拟数据（原函数保持不变）"""
    np.random.seed(42)
    random.seed(42)

    users = []
    for i in range(1, 101):
        users.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'interests': random.sample(['科技', '体育', '娱乐', '财经', '时政'], k=random.randint(2, 4))
        })
    users_df = pd.DataFrame(users)

    categories = ['科技', '体育', '娱乐', '财经', '时政']
    titles = {
        '科技': ['AI技术突破', '5G网络普及', '芯片创新', '量子计算', '人工智能'],
        '体育': ['足球比赛', '篮球直播', '奥运动态', '运动员访谈', '体育政策'],
        '娱乐': ['影视上映', '明星动态', '音乐节', '综艺节目', '娱乐八卦'],
        '财经': ['股市行情', '经济政策', '企业财报', '投资理财', '市场趋势'],
        '时政': ['国际形势', '政策解读', '社会热点', '民生新闻', '法律法规']
    }

    news = []
    for i in range(1, 501):
        cat = random.choice(categories)
        news.append({
            'news_id': i,
            'title': f"{random.choice(titles[cat])}{i}",
            'category': cat,
            'publish_time': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        })
    news_df = pd.DataFrame(news)

    behaviors = []
    for user in users:
        uid = user['user_id']
        interests = user['interests']
        for _ in range(random.randint(20, 50)):
            if random.random() < 0.8:
                cat = random.choice(interests)
                pool = news_df[news_df['category'] == cat]
            else:
                pool = news_df
            if len(pool) > 0:
                item = pool.sample(1).iloc[0]
                behaviors.append({
                    'user_id': uid,
                    'news_id': item['news_id'],
                    'action': random.choice(['click', 'click', 'click', 'like']),
                    'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M')
                })
    behaviors_df = pd.DataFrame(behaviors)

    return users_df, news_df, behaviors_df

# ========== 新增：预设场景生成 ==========

def generate_scenario(scenario_name):
    """根据场景名称生成特定数据"""
    np.random.seed(42)
    random.seed(42)

    if "场景1" in scenario_name:  # 科技媒体
        return generate_tech_media()
    elif "场景2" in scenario_name:  # 综合媒体
        return generate_balanced_media()
    elif "场景3" in scenario_name:  # 信息茧房
        return generate_echo_chamber()
    elif "场景4" in scenario_name:  # 冷启动
        return generate_cold_start()
    else:
        return generate_dataset()

def generate_tech_media():
    """场景1: 科技媒体 - 科技新闻占60%"""
    users = []
    for i in range(1, 101):
        # 90%用户关注科技
        if random.random() < 0.9:
            interests = ['科技'] + random.sample(['体育', '娱乐', '财经', '时政'], k=1)
        else:
            interests = random.sample(['科技', '体育', '娱乐', '财经', '时政'], k=2)
        users.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'interests': interests
        })
    users_df = pd.DataFrame(users)

    # 科技新闻占60%
    categories = ['科技'] * 6 + ['体育', '娱乐', '财经', '时政']
    news_df = _generate_news_with_distribution(categories)
    behaviors_df = _generate_behaviors(users, news_df, interest_prob=0.85)

    return users_df, news_df, behaviors_df

def generate_balanced_media():
    """场景2: 综合媒体 - 各类别均衡"""
    users = []
    for i in range(1, 101):
        interests = random.sample(['科技', '体育', '娱乐', '财经', '时政'], k=random.randint(2, 3))
        users.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'interests': interests
        })
    users_df = pd.DataFrame(users)

    # 均衡分布
    categories = ['科技', '体育', '娱乐', '财经', '时政']
    news_df = _generate_news_with_distribution(categories)
    behaviors_df = _generate_behaviors(users, news_df, interest_prob=0.75)

    return users_df, news_df, behaviors_df

def generate_echo_chamber():
    """场景3: 信息茧房 - 用户只看自己兴趣"""
    users = []
    for i in range(1, 101):
        # 用户兴趣更单一
        interests = random.sample(['科技', '体育', '娱乐', '财经', '时政'], k=random.randint(1, 2))
        users.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'interests': interests
        })
    users_df = pd.DataFrame(users)

    categories = ['科技', '体育', '娱乐', '财经', '时政']
    news_df = _generate_news_with_distribution(categories)
    behaviors_df = _generate_behaviors(users, news_df, interest_prob=0.95)  # 95%只看自己兴趣

    return users_df, news_df, behaviors_df

def generate_cold_start():
    """场景4: 冷启动 - 用户行为数据少"""
    users = []
    for i in range(1, 101):
        interests = random.sample(['科技', '体育', '娱乐', '财经', '时政'], k=random.randint(2, 4))
        users.append({
            'user_id': i,
            'age': random.randint(18, 60),
            'gender': random.choice(['M', 'F']),
            'interests': interests
        })
    users_df = pd.DataFrame(users)

    categories = ['科技', '体育', '娱乐', '财经', '时政']
    news_df = _generate_news_with_distribution(categories)
    behaviors_df = _generate_behaviors(users, news_df, interest_prob=0.8, min_behaviors=5, max_behaviors=15)  # 行为少

    return users_df, news_df, behaviors_df

def _generate_news_with_distribution(category_weights):
    """根据类别权重生成新闻"""
    titles = {
        '科技': ['AI技术突破', '5G网络普及', '芯片创新', '量子计算', '人工智能'],
        '体育': ['足球比赛', '篮球直播', '奥运动态', '运动员访谈', '体育政策'],
        '娱乐': ['影视上映', '明星动态', '音乐节', '综艺节目', '娱乐八卦'],
        '财经': ['股市行情', '经济政策', '企业财报', '投资理财', '市场趋势'],
        '时政': ['国际形势', '政策解读', '社会热点', '民生新闻', '法律法规']
    }

    news = []
    for i in range(1, 501):
        cat = random.choice(category_weights)
        news.append({
            'news_id': i,
            'title': f"{random.choice(titles[cat])}{i}",
            'category': cat,
            'publish_time': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(news)

def _generate_behaviors(users, news_df, interest_prob=0.8, min_behaviors=20, max_behaviors=50):
    """生成用户行为数据"""
    behaviors = []
    for user in users:
        uid = user['user_id']
        interests = user['interests']
        for _ in range(random.randint(min_behaviors, max_behaviors)):
            if random.random() < interest_prob:
                cat = random.choice(interests)
                pool = news_df[news_df['category'] == cat]
            else:
                pool = news_df
            if len(pool) > 0:
                item = pool.sample(1).iloc[0]
                behaviors.append({
                    'user_id': uid,
                    'news_id': item['news_id'],
                    'action': random.choice(['click', 'click', 'click', 'like']),
                    'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M')
                })
    return pd.DataFrame(behaviors)

# ========== 新增：信息茧房模拟 ==========

def simulate_echo_chamber(user_id, users_df, news_df, behaviors_df, iterations=5):
    """模拟信息茧房形成过程"""
    # 复制行为数据，避免修改原数据
    behaviors_copy = behaviors_df.copy()
    results = []

    for i in range(iterations):
        # 构建矩阵
        matrix = build_user_item_matrix(users_df, news_df, behaviors_copy)
        similarity = calculate_user_similarity(matrix)

        # 生成推荐
        _, recommendations = recommend_for_user(user_id, similarity, matrix, news_df, top_n=10)

        # 统计类别分布
        categories = [cat for _, _, cat, _ in recommendations]
        category_dist = {}
        for cat in ['科技', '体育', '娱乐', '财经', '时政']:
            count = categories.count(cat)
            category_dist[cat] = int(count / len(categories) * 100)

        # 用户"点击"第一条推荐
        if recommendations:
            clicked_news = recommendations[0]
            top_rec = f"{clicked_news[1]} ({clicked_news[2]})"

            # 添加新行为
            new_behavior = {
                'user_id': user_id,
                'news_id': clicked_news[0],
                'action': 'click',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            behaviors_copy = pd.concat([behaviors_copy, pd.DataFrame([new_behavior])], ignore_index=True)
        else:
            top_rec = "无推荐"

        results.append((i + 1, category_dist, top_rec))

    return results

# ========== 其他函数（保持不变） ==========

def save_dataset(users_df, news_df, behaviors_df):
    users_df.to_csv('data_users.csv', index=False)
    news_df.to_csv('data_news.csv', index=False)
    behaviors_df.to_csv('data_behaviors.csv', index=False)

def load_dataset():
    try:
        users_df = pd.read_csv('data_users.csv')
        news_df = pd.read_csv('data_news.csv')
        behaviors_df = pd.read_csv('data_behaviors.csv')
        users_df['interests'] = users_df['interests'].apply(eval)
        return users_df, news_df, behaviors_df
    except:
        return None, None, None

def build_user_item_matrix(users_df, news_df, behaviors_df):
    matrix = np.zeros((len(users_df), len(news_df)))
    for _, b in behaviors_df.iterrows():
        u_idx = b['user_id'] - 1
        n_idx = b['news_id'] - 1
        matrix[u_idx][n_idx] = 1 if b['action'] == 'click' else 2
    return matrix

def calculate_user_similarity(matrix):
    return cosine_similarity(matrix)

def recommend_for_user(user_id, similarity, matrix, news_df, top_k=5, top_n=10):
    u_idx = user_id - 1
    sims = similarity[u_idx]
    similar_indices = np.argsort(sims)[::-1][1:top_k+1]
    similar_users = [(i+1, sims[i]) for i in similar_indices]

    scores = np.zeros(len(news_df))
    for sim_idx in similar_indices:
        scores += sims[sim_idx] * matrix[sim_idx]

    user_watched = np.where(matrix[u_idx] > 0)[0]
    scores[user_watched] = -1

    top_indices = np.argsort(scores)[::-1][:top_n]

    recommendations = []
    for idx in top_indices:
        if scores[idx] > 0:
            news = news_df.iloc[idx]
            recommender = similar_users[0][0] if similar_users else user_id
            recommendations.append((
                news['news_id'],
                news['title'],
                news['category'],
                f"用户{recommender}喜欢此类内容"
            ))

    return similar_users, recommendations