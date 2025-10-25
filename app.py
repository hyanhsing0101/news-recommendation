"""
新闻推荐算法演示系统 - 主程序
添加：对比模式、信息茧房模拟、预设场景、数据查看
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils import *

st.set_page_config(page_title="新闻推荐算法演示系统", page_icon="📰", layout="wide")

# 初始化session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# ========== 侧边栏：数据管理 ==========
with st.sidebar:
    st.header("📊 数据管理")
    
    # 显示数据状态
    if st.session_state.data_loaded:
        st.success("✅ 数据已加载")
        st.metric("用户数", len(st.session_state.users_df))
        st.metric("新闻数", len(st.session_state.news_df))
        st.metric("行为记录", len(st.session_state.behaviors_df))
    else:
        st.warning("⚠️ 暂无数据")
    
    st.markdown("---")
    
    # 预设场景
    st.subheader("🎬 快速加载场景")
    
    scenario = st.selectbox(
        "选择预设场景",
        ["请选择", "场景1: 科技媒体", "场景2: 综合媒体", "场景3: 信息茧房", "场景4: 冷启动"],
        key="scenario_select"
    )
    
    if st.button("🚀 加载场景", use_container_width=True):
        if scenario != "请选择":
            with st.spinner("正在生成场景数据..."):
                users_df, news_df, behaviors_df = generate_scenario(scenario)
                save_dataset(users_df, news_df, behaviors_df)
                st.session_state.users_df = users_df
                st.session_state.news_df = news_df
                st.session_state.behaviors_df = behaviors_df
                st.session_state.data_loaded = True
                st.success(f"✅ {scenario} 加载成功！")
                st.rerun()
    
    st.markdown("---")
    
    # 原有按钮
    if st.button("🔄 生成新数据", use_container_width=True):
        with st.spinner("正在生成数据..."):
            users_df, news_df, behaviors_df = generate_dataset()
            save_dataset(users_df, news_df, behaviors_df)
            st.session_state.users_df = users_df
            st.session_state.news_df = news_df
            st.session_state.behaviors_df = behaviors_df
            st.session_state.data_loaded = True
            st.success("✅ 数据生成成功！")
            st.rerun()
    
    if st.button("📂 导入数据", use_container_width=True):
        users_df, news_df, behaviors_df = load_dataset()
        if users_df is not None:
            st.session_state.users_df = users_df
            st.session_state.news_df = news_df
            st.session_state.behaviors_df = behaviors_df
            st.session_state.data_loaded = True
            st.success("✅ 数据导入成功！")
            st.rerun()
        else:
            st.error("❌ 未找到数据文件！")

# ========== 主界面 ==========
st.title("🎯 新闻推荐算法演示系统")
st.markdown("---")

if not st.session_state.data_loaded:
    st.info("👈 请先在侧边栏加载预设场景或生成数据")
else:
    # 功能选择（添加第4个标签页）
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 单用户推荐", "⚖️ 对比模式", "🕸️ 信息茧房模拟", "📋 查看数据"])
    
    # ========== Tab1: 单用户推荐 ==========
    with tab1:
        st.header("🔍 单用户推荐演示")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            user_id = st.number_input("请输入用户ID", min_value=1, max_value=100, value=5)
            
            if st.button("🚀 开始推荐", type="primary", use_container_width=True):
                with st.spinner("正在计算..."):
                    matrix = build_user_item_matrix(
                        st.session_state.users_df,
                        st.session_state.news_df,
                        st.session_state.behaviors_df
                    )
                    similarity = calculate_user_similarity(matrix)
                    similar_users, recommendations = recommend_for_user(
                        user_id, similarity, matrix, st.session_state.news_df
                    )
                    st.session_state.similar_users = similar_users
                    st.session_state.recommendations = recommendations
        
        with col2:
            if 'recommendations' in st.session_state:
                st.subheader("📋 相似用户")
                for uid, sim in st.session_state.similar_users:
                    st.write(f"• 用户{uid} - 相似度: {sim:.2f}")
                
                st.markdown("---")
                
                st.subheader("📰 推荐结果")
                for i, (news_id, title, category, reason) in enumerate(st.session_state.recommendations, 1):
                    st.markdown(f"""
                    **{i}. {title}** ({category})  
                    💡 *推荐理由：{reason}*
                    """)
    
    # ========== Tab2: 对比模式 ==========
    with tab2:
        st.header("⚖️ 对比两个用户的推荐差异")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_a = st.number_input("用户A ID", min_value=1, max_value=100, value=5, key="user_a")
        
        with col2:
            user_b = st.number_input("用户B ID", min_value=1, max_value=100, value=10, key="user_b")
        
        if st.button("🔄 开始对比", type="primary", use_container_width=True):
            with st.spinner("正在计算对比结果..."):
                matrix = build_user_item_matrix(
                    st.session_state.users_df,
                    st.session_state.news_df,
                    st.session_state.behaviors_df
                )
                similarity = calculate_user_similarity(matrix)
                
                similar_a, rec_a = recommend_for_user(user_a, similarity, matrix, st.session_state.news_df)
                similar_b, rec_b = recommend_for_user(user_b, similarity, matrix, st.session_state.news_df)
                
                st.session_state.compare_a = (user_a, rec_a)
                st.session_state.compare_b = (user_b, rec_b)
        
        if 'compare_a' in st.session_state:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"👤 用户{st.session_state.compare_a[0]}")
                user_info_a = st.session_state.users_df[st.session_state.users_df['user_id'] == st.session_state.compare_a[0]].iloc[0]
                st.write(f"**兴趣**: {', '.join(user_info_a['interests'])}")
                st.markdown("**推荐结果**:")
                for i, (_, title, cat, _) in enumerate(st.session_state.compare_a[1][:5], 1):
                    st.write(f"{i}. {title} ({cat})")
            
            with col2:
                st.subheader(f"👤 用户{st.session_state.compare_b[0]}")
                user_info_b = st.session_state.users_df[st.session_state.users_df['user_id'] == st.session_state.compare_b[0]].iloc[0]
                st.write(f"**兴趣**: {', '.join(user_info_b['interests'])}")
                st.markdown("**推荐结果**:")
                for i, (_, title, cat, _) in enumerate(st.session_state.compare_b[1][:5], 1):
                    st.write(f"{i}. {title} ({cat})")
            
            st.markdown("---")
            st.subheader("📊 差异分析")
            cats_a = [cat for _, _, cat, _ in st.session_state.compare_a[1][:5]]
            cats_b = [cat for _, _, cat, _ in st.session_state.compare_b[1][:5]]
            
            common = set(cats_a) & set(cats_b)
            if common:
                st.info(f"共同类别: {', '.join(common)}")
            else:
                st.warning("⚠️ 两个用户的推荐结果完全不同！这就是个性化推荐。")
    
    # ========== Tab3: 信息茧房模拟 ==========
    with tab3:
        st.header("🕸️ 信息茧房形成过程模拟")
        st.info("模拟用户持续点击推荐内容，观察推荐如何越来越集中")
        
        user_id_sim = st.number_input("选择用户ID", min_value=1, max_value=100, value=5, key="sim_user")
        iterations = st.slider("模拟次数", min_value=3, max_value=10, value=5)
        
        if st.button("▶️ 开始模拟", type="primary"):
            with st.spinner("正在模拟..."):
                results = simulate_echo_chamber(
                    user_id_sim,
                    st.session_state.users_df,
                    st.session_state.news_df,
                    st.session_state.behaviors_df,
                    iterations
                )
                st.session_state.sim_results = results
        
        if 'sim_results' in st.session_state:
            st.markdown("---")
            st.subheader("📈 茧房形成过程")
            
            for i, (iter_num, category_dist, top_rec) in enumerate(st.session_state.sim_results):
                with st.expander(f"第 {iter_num} 次推荐", expanded=(i == 0 or i == len(st.session_state.sim_results) - 1)):
                    st.write("**类别分布**:")
                    for cat, pct in category_dist.items():
                        st.progress(pct / 100, text=f"{cat}: {pct}%")
                    st.write(f"**用户点击**: {top_rec}")
            
            st.markdown("---")
            st.warning("⚠️ **观察**: 推荐内容越来越集中在用户感兴趣的类别，这就是信息茧房的形成过程！")
    
    # ========== Tab4: 查看数据 ==========
    with tab4:
        st.header("📋 数据总览")
        
        data_view = st.selectbox("选择查看", ["用户数据", "新闻数据", "行为数据", "数据统计"])
        
        if data_view == "用户数据":
            st.subheader("👥 用户列表")
            st.dataframe(st.session_state.users_df, use_container_width=True)
            
        elif data_view == "新闻数据":
            st.subheader("📰 新闻列表")
            st.dataframe(st.session_state.news_df, use_container_width=True)
            
        elif data_view == "行为数据":
            st.subheader("📊 用户行为记录（前100条）")
            st.dataframe(st.session_state.behaviors_df.head(100), use_container_width=True)
            
        elif data_view == "数据统计":
            st.subheader("📈 数据统计分析")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总用户数", len(st.session_state.users_df))
            with col2:
                st.metric("总新闻数", len(st.session_state.news_df))
            with col3:
                st.metric("总行为数", len(st.session_state.behaviors_df))
            
            st.markdown("---")
            st.subheader("📊 新闻类别分布")
            category_counts = st.session_state.news_df['category'].value_counts()
            st.bar_chart(category_counts)
            
            st.markdown("---")
            st.subheader("📊 用户行为类型分布")
            action_counts = st.session_state.behaviors_df['action'].value_counts()
            st.bar_chart(action_counts)
