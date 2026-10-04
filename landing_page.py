import streamlit as st


def run_landing_page():
    # --- STYLING INJECTION ---
    st.markdown(
        """
        <style>
        /* Hero Banner Container */
        .hero-container {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
        }
        
        .hero-tag {
            font-size: 0.85rem;
            font-weight: 700;
            color: #38BDF8;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .hero-title {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin-bottom: 16px !important;
            line-height: 1.2 !important;
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #94A3B8;
            max-width: 650px;
            margin: 0 auto 30px auto;
            line-height: 1.6;
        }

        /* Section Headings */
        .section-header {
            text-align: center;
            margin: 40px 0 30px 0;
        }

        .section-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #0F172A;
        }

        /* Feature Cards Grid */
        .feature-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            height: 100%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease;
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 12px;
        }

        .feature-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 8px;
        }

        .feature-desc {
            font-size: 0.9rem;
            color: #64748B;
            line-height: 1.5;
        }

        /* Team Banner */
        .team-banner {
            background: #0F172A;
            border-radius: 20px;
            padding: 40px 30px;
            color: #FFFFFF;
            text-align: center;
            margin-top: 50px;
        }

        .team-title {
            color: #FFFFFF !important;
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .team-sub {
            color: #94A3B8;
            font-size: 0.9rem;
            margin-bottom: 30px;
        }

        .member-card {
            background: #1E293B;
            border-radius: 14px;
            padding: 20px 10px;
            text-align: center;
            border: 1px solid #334155;
        }

        .member-avatar {
            width: 50px;
            height: 50px;
            background: #2563EB;
            color: #FFFFFF;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.2rem;
            margin: 0 auto 12px auto;
        }

        .member-name {
            font-weight: 700;
            color: #FFFFFF;
            font-size: 0.95rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # --- HERO HEADER SECTION ---
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-tag">AIML MAJOR PROJECT 2026</div>
            <div class="hero-title">Intelligent Reading Platform</div>
            <div class="hero-subtitle">
                AI-powered reading assistance, vocabulary vault, and emotion-aware tracking for smarter learning.
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # --- BUTTONS UNDER HERO ---
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.info("Use the sidebar menu to register or log in.")
    with col4:
        if st.button("🔐 Login", use_container_width=True):
            st.info("Select Login from the sidebar menu.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # --- FEATURE CARDS SECTION ---
    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">What Our Platform Does For You</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Emotion Tracking</div>
                <div class="feature-desc">Detect reading state and focus levels with AI vision monitoring.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with f_col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Vocabulary Vault</div>
                <div class="feature-desc">Save challenging words automatically for spaced repetition quizzes.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with f_col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Streak & Goals</div>
                <div class="feature-desc">Track daily reading habits, streak milestones, and earn reader badges.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with f_col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">👩‍🏫</div>
                <div class="feature-title">Educator Portal</div>
                <div class="feature-desc">Provide teachers with student analytics, exports, and progress reports.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # --- TEAM SECTION ---
    st.markdown(
        """
        <div class="team-banner">
            <div class="team-title">Project Team</div>
            <div class="team-sub">Department of CSE (AIML) | Final Year 2026</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    t_col1, t_col2, t_col3, t_col4 = st.columns(4)

    with t_col1:
        st.markdown(
            """
            <div class="member-card">
                <div class="member-avatar">S</div>
                <div class="member-name">Student Lead</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with t_col2:
        st.markdown(
            """
            <div class="member-card">
                <div class="member-avatar">M</div>
                <div class="member-name">ML Developer</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with t_col3:
        st.markdown(
            """
            <div class="member-card">
                <div class="member-avatar">U</div>
                <div class="member-name">UI Engineer</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with t_col4:
        st.markdown(
            """
            <div class="member-card">
                <div class="member-avatar">D</div>
                <div class="member-name">Data Analyst</div>
            </div>
        """,
            unsafe_allow_html=True,
        )