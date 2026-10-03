if col3.button("Show Full Report"):
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        df = pd.read_csv(FILE_NAME)
        
        st.subheader("📊 Student Performance Dashboard")
        
        # Create two columns for the dashboard
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. Pie Chart: Overall Emotional Experience
            st.write("### Emotion Distribution")
            fig_pie = px.pie(df, names='Emotion', 
                             color='Emotion',
                             color_discrete_map={'HAPPY':'green', 'SAD':'red', 'NEUTRAL':'gray', 'FRUSTRATED':'orange', 'CONFUSED':'blue', 'SURPRISED':'yellow'},
                             hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            # 2. Bar Chart: Emotion Frequency
            st.write("### Emotion Frequency Count")
            emotion_counts = df['Emotion'].value_counts().reset_index()
            emotion_counts.columns = ['Emotion', 'Count']
            fig_bar = px.bar(emotion_counts, x='Emotion', y='Count', color='Emotion')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        # 3. Raw Data Table
        st.write("### Full Session History")
        st.dataframe(df.sort_values(by='Timestamp', ascending=False), use_container_width=True)
        
        # 4. Summary Metric
        total_sessions = len(df)
        st.metric("Total Emotion Data Points Captured", total_sessions)
    else:
        st.warning("No performance data found yet. Start a session to generate a report!")