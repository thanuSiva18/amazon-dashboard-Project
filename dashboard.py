import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Page setup with custom theme
st.set_page_config(
    page_title="Amazon Analytics Hub", 
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main title styling */
    .main-header {
        background: linear-gradient(90deg, #FF9500 0%, #FF6B35 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Metric cards styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #FF9500;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    
    /* Filter expanders */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    /* Product cards */
    .product-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .product-card:hover {
        border-color: #FF9500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        padding: 1rem 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF9500 !important;
        color: white !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🛒 Amazon Analytics Hub</h1>
    <p>Comprehensive E-Commerce Data Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = r"C:\Users\thanu\OneDrive\Desktop\folders\E-com dashboard project\amazon.csv"
    if not os.path.exists(file_path):
        st.error(f"📁 File not found: {file_path}")
        st.info("💡 Please ensure the CSV file exists at the specified path.")
        st.stop()
    
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        
        # Data cleaning with progress indicator
        with st.spinner('🔄 Processing data...'):
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            df = df.dropna(subset=['rating'])
            df['discount_percentage'] = df['discount_percentage'].astype(str).str.replace('%', '', regex=False)
            df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')
            df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')
            df['rating_count'].fillna(0, inplace=True)
            df['category'] = df['category'].astype(str)
            df['product_name'] = df['product_name'].astype(str)
            
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

# Load data
df = load_data()

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #FF9500, #FF6B35); 
                border-radius: 10px; margin-bottom: 1rem;'>
        <h3 style='color: white; margin: 0;'>🎯 Smart Filters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Category and Rating Filters
    with st.expander("📊 Category & Rating", expanded=True):
        categories = st.multiselect(
            "🏷️ Select Categories", 
            options=sorted(df['category'].unique()), 
            default=sorted(df['category'].unique()),
            help="Choose one or more categories to analyze"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            min_rating = st.number_input(
                "⭐ Min Rating", 
                min_value=float(df['rating'].min()),
                max_value=float(df['rating'].max()),
                value=float(df['rating'].min()),
                step=0.1
            )
        with col2:
            max_rating = st.number_input(
                "⭐ Max Rating", 
                min_value=float(df['rating'].min()),
                max_value=float(df['rating'].max()),
                value=float(df['rating'].max()),
                step=0.1
            )
    
    # Product Search
    with st.expander("🔍 Product Search"):
        search_term = st.text_input(
            "Search products...", 
            placeholder="Enter product name or keyword",
            help="Search for specific products by name"
        )
        
        # Advanced filters
        st.subheader("🎛️ Advanced Filters")
        min_discount = st.slider(
            "💸 Minimum Discount %", 
            0.0, float(df['discount_percentage'].max()), 
            0.0
        )
        
        min_reviews = st.slider(
            "👥 Minimum Reviews", 
            0, int(df['rating_count'].max()), 
            0,
            step=10
        )
    
    # Sorting Options
    with st.expander("🔄 Sort & Display", expanded=True):
        sort_by = st.selectbox(
            "📈 Sort by", 
            ["rating", "discount_percentage", "rating_count"],
            format_func=lambda x: {"rating": "⭐ Rating", "discount_percentage": "💸 Discount", "rating_count": "👥 Reviews"}[x]
        )
        sort_order = st.radio("📊 Order", ["Descending", "Ascending"])
        
        items_to_show = st.selectbox("📱 Items to display", [10, 20, 50, 100], index=0)
    
    # Download Section
    st.markdown("---")
    st.markdown("### 📥 Export Data")
    
    # Filter the data for export
    filtered_export_df = df[
        (df['category'].isin(categories)) &
        (df['rating'] >= min_rating) & (df['rating'] <= max_rating) &
        (df['discount_percentage'] >= min_discount) &
        (df['rating_count'] >= min_reviews)
    ]
    
    if search_term:
        filtered_export_df = filtered_export_df[
            filtered_export_df['product_name'].str.contains(search_term, case=False, na=False)
        ]
    
    st.download_button(
        "⬇️ Download Filtered Data",
        data=filtered_export_df.to_csv(index=False).encode('utf-8'),
        file_name=f"amazon_filtered_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Apply all filters
@st.cache_data
def filter_data(categories, min_rating, max_rating, search_term, min_discount, min_reviews):
    filtered_df = df[
        (df['category'].isin(categories)) &
        (df['rating'] >= min_rating) & (df['rating'] <= max_rating) &
        (df['discount_percentage'] >= min_discount) &
        (df['rating_count'] >= min_reviews)
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['product_name'].str.contains(search_term, case=False, na=False)
        ]
    
    return filtered_df

# Get filtered data
filtered_df = filter_data(categories, min_rating, max_rating, search_term, min_discount, min_reviews)

# Check if data is available
if filtered_df.empty:
    st.warning("⚠️ No products match your current filters. Please adjust your criteria.")
    st.stop()

# Key Performance Indicators
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown("""
    <div class="metric-container">
        <h4 style='color: #FF9500; margin: 0;'>📦 Total Products</h4>
        <h2 style='margin: 0.5rem 0;'>{:,}</h2>
        <p style='color: #6c757d; margin: 0;'>Products Found</p>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)

with kpi_col2:
    avg_rating = filtered_df['rating'].mean()
    st.markdown("""
    <div class="metric-container">
        <h4 style='color: #28a745; margin: 0;'>⭐ Avg Rating</h4>
        <h2 style='margin: 0.5rem 0;'>{:.2f}</h2>
        <p style='color: #6c757d; margin: 0;'>Out of 5.0</p>
    </div>
    """.format(avg_rating), unsafe_allow_html=True)

with kpi_col3:
    avg_discount = filtered_df['discount_percentage'].mean()
    st.markdown("""
    <div class="metric-container">
        <h4 style='color: #dc3545; margin: 0;'>💸 Avg Discount</h4>
        <h2 style='margin: 0.5rem 0;'>{:.1f}%</h2>
        <p style='color: #6c757d; margin: 0;'>Average Savings</p>
    </div>
    """.format(avg_discount), unsafe_allow_html=True)

with kpi_col4:
    total_reviews = int(filtered_df['rating_count'].sum())
    st.markdown("""
    <div class="metric-container">
        <h4 style='color: #17a2b8; margin: 0;'>👥 Total Reviews</h4>
        <h2 style='margin: 0.5rem 0;'>{:,}</h2>
        <p style='color: #6c757d; margin: 0;'>Customer Reviews</p>
    </div>
    """.format(total_reviews), unsafe_allow_html=True)

with kpi_col5:
    max_discount = filtered_df['discount_percentage'].max()
    st.markdown("""
    <div class="metric-container">
        <h4 style='color: #6f42c1; margin: 0;'>🏆 Max Discount</h4>
        <h2 style='margin: 0.5rem 0;'>{:.0f}%</h2>
        <p style='color: #6c757d; margin: 0;'>Best Deal</p>
    </div>
    """.format(max_discount), unsafe_allow_html=True)

# Main Dashboard Content
st.markdown('<div class="section-header">📊 Visual Analytics Dashboard</div>', unsafe_allow_html=True)

# Row 1: Category Analysis
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    category_counts = filtered_df['category'].value_counts().head(10).reset_index()
    category_counts.columns = ['category', 'count']
    
    fig_pie = px.pie(
        category_counts, 
        names='category', 
        values='count', 
        title="🧩 Product Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        showlegend=True,
        height=400,
        font_size=12,
        title_font_size=16,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    category_rating = filtered_df.groupby('category')['rating'].mean().sort_values(ascending=False).head(10).reset_index()
    
    fig_bar = px.bar(
        category_rating,
        x='rating',
        y='category',
        orientation='h',
        title="⭐ Average Rating by Category",
        color='rating',
        color_continuous_scale='RdYlGn',
        text='rating'
    )
    fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='inside')
    fig_bar.update_layout(
        height=400,
        yaxis={'categoryorder':'total ascending'},
        title_font_size=16,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Scatter Plot Analysis
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_scatter = px.scatter(
    filtered_df.head(1000),  # Limit points for performance
    x='discount_percentage',
    y='rating',
    color='category',
    size='rating_count',
    hover_data=['product_name'],
    title="📉 Discount vs Rating Analysis (Size = Review Count)",
    opacity=0.7
)

# Add correlation annotation
correlation_coef = filtered_df['rating'].corr(filtered_df['discount_percentage'])
fig_scatter.add_annotation(
    text=f"Correlation: {correlation_coef:.3f}",
    xref="paper", yref="paper",
    x=0.02, y=0.98,
    showarrow=False,
    font=dict(size=14, color="red"),
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="red",
    borderwidth=1
)

fig_scatter.update_layout(
    height=500,
    title_font_size=16,
    margin=dict(t=50, b=20, l=20, r=20)
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Advanced Analytics Tabs
st.markdown('<div class="section-header">🔬 Advanced Analytics</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏷️ Discount Insights", "🔗 Correlations", "📊 Distributions", "🏆 Top Performers"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        top_discounted = filtered_df.nlargest(15, 'discount_percentage')
        top_discounted['short_name'] = top_discounted['product_name'].apply(
            lambda x: (x[:30] + '...') if len(x) > 30 else x
        )
        
        fig_discount_bar = px.bar(
            top_discounted,
            x='discount_percentage',
            y='short_name',
            color='rating',
            color_continuous_scale='RdYlGn',
            orientation='h',
            title="🏷️ Top 15 Highest Discounted Products",
            hover_data=['category', 'rating_count']
        )
        fig_discount_bar.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=600,
            title_font_size=14,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_discount_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_discount_box = px.box(
            filtered_df,
            x='category',
            y='discount_percentage',
            title="📦 Discount Distribution by Category",
            color='category'
        )
        fig_discount_box.update_xaxes(tickangle=45)
        fig_discount_box.update_layout(
            showlegend=False,
            height=600,
            title_font_size=14,
            margin=dict(t=40, b=100, l=20, r=20)
        )
        st.plotly_chart(fig_discount_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Correlation heatmap
        numeric_cols = ['rating', 'discount_percentage', 'rating_count']
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdYlBu_r',
            title="🔥 Feature Correlation Matrix"
        )
        fig_heatmap.update_layout(height=400, title_font_size=14)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Category performance radar chart
        category_stats = filtered_df.groupby('category').agg({
            'rating': 'mean',
            'discount_percentage': 'mean',
            'rating_count': 'mean'
        }).head(8)
        
        # Normalize the data for radar chart
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        normalized_stats = scaler.fit_transform(category_stats)
        
        fig_radar = go.Figure()
        
        for i, category in enumerate(category_stats.index):
            fig_radar.add_trace(go.Scatterpolar(
                r=normalized_stats[i],
                theta=['Rating', 'Discount %', 'Review Count'],
                fill='toself',
                name=category[:15] + ('...' if len(category) > 15 else '')
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title="🎯 Category Performance Radar",
            height=400,
            title_font_size=14
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_hist_rating = px.histogram(
            filtered_df,
            x='rating',
            nbins=25,
            title="📊 Rating Distribution",
            color_discrete_sequence=['#FF9500']
        )
        
        mean_rating = filtered_df['rating'].mean()
        fig_hist_rating.add_vline(
            x=mean_rating, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Mean: {mean_rating:.2f}"
        )
        
        fig_hist_rating.update_layout(
            height=400,
            bargap=0.1,
            title_font_size=14,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_hist_rating, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Only show products with reviews > 0 for meaningful distribution
        products_with_reviews = filtered_df[filtered_df['rating_count'] > 0]
        
        fig_hist_reviews = px.histogram(
            products_with_reviews,
            x='rating_count',
            title="👥 Review Count Distribution",
            nbins=30,
            color_discrete_sequence=['#28a745']
        )
        fig_hist_reviews.update_xaxes(type="log", title="Review Count (Log Scale)")
        fig_hist_reviews.update_layout(
            height=400,
            bargap=0.1,
            title_font_size=14,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_hist_reviews, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    # Top products section with enhanced layout
    st.markdown("### 🏆 Top Performing Products")
    
    # Sort and get top products
    top_products = filtered_df.sort_values(
        by=sort_by, ascending=(sort_order == "Ascending")
    ).head(items_to_show)
    
    # Enhanced metrics
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        best_rated = filtered_df.loc[filtered_df['rating'].idxmax()]
        st.metric("🥇 Best Rated", f"{best_rated['rating']:.1f}⭐", 
                 delta=f"+{best_rated['rating'] - filtered_df['rating'].mean():.2f}")
    
    with metrics_col2:
        highest_discount = filtered_df.loc[filtered_df['discount_percentage'].idxmax()]
        st.metric("💰 Best Discount", f"{highest_discount['discount_percentage']:.0f}%")
    
    with metrics_col3:
        most_reviewed = filtered_df.loc[filtered_df['rating_count'].idxmax()]
        st.metric("👑 Most Reviewed", f"{int(most_reviewed['rating_count']):,}")
    
    with metrics_col4:
        avg_price_category = filtered_df.groupby('category')['discount_percentage'].mean().idxmax()
        st.metric("🎯 Best Category", avg_price_category[:15])
    
    # Products display
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### 📋 Detailed Products Table")
        
        # Enhanced dataframe display
        display_df = top_products[['product_name', 'category', 'rating', 'discount_percentage', 'rating_count']].copy()
        display_df['rating'] = display_df['rating'].round(2)
        display_df['discount_percentage'] = display_df['discount_percentage'].round(1)
        display_df['rating_count'] = display_df['rating_count'].astype(int)
        display_df.columns = ['📦 Product Name', '🏷️ Category', '⭐ Rating', '💸 Discount %', '👥 Reviews']
        
        # Style the dataframe
        styled_df = display_df.style.format({
            '⭐ Rating': '{:.1f}',
            '💸 Discount %': '{:.1f}%',
            '👥 Reviews': '{:,}'
        }).background_gradient(subset=['⭐ Rating'], cmap='RdYlGn', vmin=0, vmax=5)
        
        st.dataframe(styled_df, use_container_width=True, height=400)
    
    with col2:
        st.markdown("#### 📊 Quick Insights")
        
        # Top 5 chart
        chart_data = top_products.head(5).copy()
        chart_data['short_name'] = chart_data['product_name'].apply(
            lambda x: x[:20] + '...' if len(x) > 20 else x
        )
        
        fig_top_chart = px.bar(
            chart_data,
            x=sort_by,
            y='short_name',
            orientation='h',
            title=f"Top 5 by {sort_by.title()}",
            color=sort_by,
            color_continuous_scale='viridis'
        )
        fig_top_chart.update_layout(
            height=350,
            yaxis={'categoryorder':'total ascending'},
            title_font_size=12,
            margin=dict(t=30, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_top_chart, use_container_width=True)

# Product Cards Section
st.markdown('<div class="section-header">🛍️ Featured Products</div>', unsafe_allow_html=True)

# Display top 6 products as cards
top_featured = filtered_df.sort_values('rating', ascending=False).head(6)

for i in range(0, len(top_featured), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(top_featured):
            product = top_featured.iloc[i + j]
            with col:
                st.markdown(f"""
                <div class="product-card">
                    <h4 style='color: #FF9500; margin-top: 0;'>{product['product_name'][:50]}{'...' if len(product['product_name']) > 50 else ''}</h4>
                    <p><strong>Category:</strong> {product['category']}</p>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 15px; font-size: 0.9rem;'>
                            ⭐ {product['rating']:.1f}/5.0
                        </span>
                        <span style='background: #dc3545; color: white; padding: 0.2rem 0.5rem; border-radius: 15px; font-size: 0.9rem;'>
                            💸 {product['discount_percentage']:.0f}% OFF
                        </span>
                    </div>
                    <p style='margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;'>
                        👥 {int(product['rating_count']):,} reviews
                    </p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; margin-top: 2rem; color: white;'>
    <h3 style='margin: 0; color: white;'>🚀 Amazon Analytics Hub</h3>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Built with ❤️ by Thanu | AI & Data Science Enthusiast</p>
    <p style='margin: 0.25rem 0 0 0; opacity: 0.8; font-size: 0.9rem;'>Empowering businesses with data-driven insights</p>
</div>
""", unsafe_allow_html=True)

# Additional insights sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 Quick Insights")
    
    if not filtered_df.empty:
        # Calculate insights
        total_categories = len(filtered_df['category'].unique())
        avg_reviews_per_product = filtered_df['rating_count'].mean()
        high_rated_products = len(filtered_df[filtered_df['rating'] >= 4.0])
        
        st.info(f"📊 **{total_categories}** unique categories")
        st.info(f"👥 **{avg_reviews_per_product:.0f}** avg reviews per product")
        st.info(f"⭐ **{high_rated_products}** products rated 4.0+")
        
        # Top category by average rating
        top_category = filtered_df.groupby('category')['rating'].mean().idxmax()
        st.success(f"🏆 **{top_category}** has the highest average rating")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This dashboard provides comprehensive analytics for Amazon e-commerce data including:
    
    - 📊 **Interactive Visualizations**
    - 🔍 **Advanced Filtering**
    - 📈 **Performance Metrics**
    - 💡 **Business Insights**
    - 📱 **Responsive Design**
    """)

# Add data quality indicators
if st.checkbox("🔍 Show Data Quality Report", value=False):
    st.markdown('<div class="section-header">📋 Data Quality Report</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Completeness")
        completeness = {
            'Product Name': (df['product_name'].notna().sum() / len(df)) * 100,
            'Category': (df['category'].notna().sum() / len(df)) * 100,
            'Rating': (df['rating'].notna().sum() / len(df)) * 100,
            'Discount': (df['discount_percentage'].notna().sum() / len(df)) * 100,
            'Review Count': (df['rating_count'].notna().sum() / len(df)) * 100
        }
        
        for field, percentage in completeness.items():
            color = "🟢" if percentage > 95 else "🟡" if percentage > 80 else "🔴"
            st.write(f"{color} {field}: {percentage:.1f}%")
    
    with col2:
        st.markdown("#### 📈 Distribution Stats")
        st.write(f"**Total Records:** {len(df):,}")
        st.write(f"**Filtered Records:** {len(filtered_df):,}")
        st.write(f"**Categories:** {df['category'].nunique()}")
        st.write(f"**Rating Range:** {df['rating'].min():.1f} - {df['rating'].max():.1f}")
        st.write(f"**Discount Range:** {df['discount_percentage'].min():.1f}% - {df['discount_percentage'].max():.1f}%")
    
    with col3:
        st.markdown("#### ⚠️ Data Issues")
        issues = []
        
        # Check for potential issues
        zero_discounts = len(df[df['discount_percentage'] == 0])
        if zero_discounts > len(df) * 0.1:
            issues.append(f"🟡 {zero_discounts:,} products with 0% discount")
        
        no_reviews = len(df[df['rating_count'] == 0])
        if no_reviews > 0:
            issues.append(f"🟡 {no_reviews:,} products without reviews")
        
        extreme_discounts = len(df[df['discount_percentage'] > 80])
        if extreme_discounts > 0:
            issues.append(f"🟡 {extreme_discounts:,} products with >80% discount")
        
        if not issues:
            st.success("✅ No major data quality issues detected!")
        else:
            for issue in issues:
                st.warning(issue)

# Performance optimization notice
if len(filtered_df) > 5000:
    st.info("💡 **Performance Note:** Large dataset detected. Some visualizations show a sample of data for optimal performance.")

# Last updated info
st.markdown(f"""
<div style='text-align: center; color: #6c757d; font-size: 0.8rem; margin-top: 1rem;'>
    Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | 
    Showing {len(filtered_df):,} of {len(df):,} products
</div>
""", unsafe_allow_html=True)