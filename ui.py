import streamlit as st


def render_header(title: str, subtitle: str, icon: str = "🎓"):
  """Renders a sleek page title banner."""
  st.markdown(
      f"""
        <div style="margin-bottom: 28px;">
            <h1 style="font-size: 2.1rem; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; margin-bottom: 4px;">
                {icon} {title}
            </h1>
            <p style="color: #64748B; font-size: 0.98rem; margin: 0;">{subtitle}</p>
        </div>
    """,
      unsafe_allow_html=True,
  )


def render_stat_card(title: str, value: str, badge_text: str = ""):
  """Renders a metric container card."""
  badge_html = (
      f'<span class="stat-badge">{badge_text}</span>' if badge_text else ""
  )
  st.markdown(
      f"""
        <div class="stat-widget">
            <div class="stat-header">
                <span class="stat-title">{title}</span>
                {badge_html}
            </div>
            <div class="stat-value">{value}</div>
        </div>
    """,
      unsafe_allow_html=True,
  )


def render_card_start(title: str = ""):
  """Opens a white card container block."""
  title_html = (
      f'<h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A;'
      f' margin-bottom: 18px;">{title}</h3>'
      if title
      else ""
  )
  st.markdown(
      f"""
        <div class="saas-card">
            {title_html}
    """,
      unsafe_allow_html=True,
  )


def render_card_end():
  """Closes a white card container block."""
  st.markdown("</div>", unsafe_allow_html=True)