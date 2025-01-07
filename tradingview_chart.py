import streamlit as st
import streamlit.components.v1 as components
from tradingview_ta import TA_Handler
import pandas as pd

# 必须首先调用 set_page_config
st.set_page_config(
    page_title="多币种行情监控",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# 然后是自定义CSS样式
st.markdown("""
    <style>
        /* 全局黑色背景 */
        .stApp {
            background-color: #000000 !important;
            color: #e0e0e0 !important;
        }
        /* 移除所有顶部空间 */
        .main {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background-color: #000000 !important;
        }
        .main > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
            background-color: #000000 !important;
        }
        .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
            padding-bottom: 0 !important;
            background-color: #000000 !important;
        }
        /* 隐藏Streamlit默认的header */
        header {
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        #root > div:first-child {
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        /* 标题样式 */
        h1 {
            font-size: 1.2rem !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
            color: #e0e0e0 !important;
        }
        h3 {
            font-size: 0.7rem !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            color: #e0e0e0 !important;
        }
        /* 控制图表容器间距 */
        div[data-testid="column"] {
            padding: 0 0.1rem !important;  /* 减小列间距 */
            margin: 0 !important;
        }
        div[data-testid="stVerticalBlock"] > div {
            padding: 0 !important;
            margin: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div {
            padding: 0 !important;
            margin: 0 !important;
        }
        .element-container {
            margin: 0 !important;
        }
        /* 控制图表之间的垂直间距 */
        .tradingview-widget-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        /* 减小行间距 */
        div.row-widget {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        /* 控制整体布局 */
        section[data-testid="stSidebar"] {
            margin: 0 !important;
            padding: 0 !important;
            background-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }
        .sidebar .sidebar-content {
            background-color: #1a1a1a !important;
        }
        .stApp {
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-layout="wide"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        iframe {
            margin: 0 !important;
            padding: 0 !important;
        }
        /* 确保内容从顶部开始 */
        [data-testid="stAppViewContainer"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

def get_tradingview_widget(symbol, height=400):
    # 优化 TradingView Widget 配置
    widget_html = f"""
    <div class="tradingview-widget-container" style="margin-bottom:-10px;">
        <div id="tradingview_{symbol.replace(':', '_')}"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "width": "100%",
            "height": {height},
            "symbol": "{symbol}",
            "interval": "60",          // 使用1小时K线
            "timezone": "Asia/Shanghai",
            "theme": "dark",           // 改为深色主题
            "style": "0",             // 使用空心K线
            "locale": "zh_CN",
            "toolbar_bg": "#000000",   // 工具栏背景改为黑色
            "enable_publishing": false,
            "hide_top_toolbar": true,
            "hide_legend": true,
            "hide_side_toolbar": true,
            "allow_symbol_change": false,
            "save_image": false,
            "container_id": "tradingview_{symbol.replace(':', '_')}",
            "hide_volume": true,      // 隐藏成交量
            "hide_drawing_toolbar": true,
            "range": "12H",           // 只加载12小时数据
            "enabled_features": [],
            "disabled_features": [
                "header_symbol_search",
                "symbol_search_hot_key",
                "header_chart_type",
                "header_compare",
                "header_interval_dialog_button",
                "show_interval_dialog_on_key_press",
                "header_resolutions",
                "header_indicators",
                "header_settings",
                "header_fullscreen_button",
                "header_screenshot",
                "timeframes_toolbar",
                "volume_force_overlay",
                "show_logo_on_all_charts",
                "legend_widget",
                "main_series_scale_menu",
                "scales_context_menu",
                "show_chart_property_page",
                "chart_crosshair_menu",
                "chart_events",
                "header_widget_dom_node",
                "source_selection_markers",
                "go_to_date"
            ],
            "overrides": {{
                "mainSeriesProperties.candleStyle.upColor": "#26a69a",
                "mainSeriesProperties.candleStyle.downColor": "#ef5350",
                "mainSeriesProperties.candleStyle.drawWick": true,
                "mainSeriesProperties.candleStyle.drawBorder": true,
                "mainSeriesProperties.candleStyle.borderUpColor": "#26a69a",
                "mainSeriesProperties.candleStyle.borderDownColor": "#ef5350",
                "mainSeriesProperties.candleStyle.wickUpColor": "#26a69a",
                "mainSeriesProperties.candleStyle.wickDownColor": "#ef5350",
                "paneProperties.background": "#000000",          // 图表背景改为黑色
                "paneProperties.vertGridProperties.color": "#1a1a1a",  // 网格线改为深色
                "paneProperties.horzGridProperties.color": "#1a1a1a",
                "scalesProperties.textColor": "#666666",         // 刻度文字改为灰色
                "scalesProperties.backgroundColor": "#000000"    // 刻度背景改为黑色
            }},
            "loading_screen": {{"backgroundColor": "#000000"}}   // 加载背景改为黑色
        }});
        </script>
    </div>
    """
    return widget_html

def main():
    # 标题（使用更小的标题）
    st.markdown("<h1 style='margin:0;padding:0;'>多币种实时行情监控</h1>", unsafe_allow_html=True)
    
    # 创建默认交易对列表
    default_pairs = [
        "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:BNBUSDT", 
        "BINANCE:SOLUSDT", "BINANCE:DOGEUSDT", "BINANCE:ADAUSDT", 
        "BINANCE:DOTUSDT", "BINANCE:MATICUSDT", "BINANCE:LINKUSDT", 
        "BINANCE:AVAXUSDT", "BINANCE:TRXUSDT", "BINANCE:ATOMUSDT",
        "BINANCE:LTCUSDT", "BINANCE:UNIUSDT", "BINANCE:XRPUSDT",
        "BINANCE:SHIBUSDT", "BINANCE:AAVEUSDT", "BINANCE:ALGOUSDT",
        "BINANCE:APTUSDT", "BINANCE:ARBUSDT", "BINANCE:FILUSDT",
        "BINANCE:FTMUSDT", "BINANCE:NEARUSDT", "BINANCE:OPUSDT"
    ]
    
    # 侧边栏配置
    with st.sidebar:
        st.header("配置选项")
        display_mode = st.radio("显示方式", ["网格显示", "列表显示"])
        selected_pairs = st.multiselect(
            "选择要显示的交易对",
            [pair for pair in default_pairs],
            default=default_pairs
        )
        charts_per_row = 3  # 固定为3列

    # 减小图表高度
    chart_height = 180 if display_mode == "网格显示" else 300  # 降低网格模式下的图表高度

    # 主界面显示
    if display_mode == "网格显示":
        with st.container():
            for i in range(0, len(selected_pairs), charts_per_row):
                cols = st.columns(charts_per_row)
                for j in range(charts_per_row):
                    if i + j < len(selected_pairs):
                        with cols[j]:
                            symbol = selected_pairs[i + j]
                            display_symbol = symbol.replace("BINANCE:", "")
                            st.markdown(f"<h3>{display_symbol}</h3>", unsafe_allow_html=True)
                            components.html(
                                get_tradingview_widget(symbol, height=chart_height),
                                height=chart_height + 5
                            )
    else:
        for symbol in selected_pairs:
            display_symbol = symbol.replace("BINANCE:", "")
            st.markdown(f"<h3>{display_symbol}</h3>", unsafe_allow_html=True)
            components.html(
                get_tradingview_widget(symbol, height=chart_height),
                height=chart_height + 20
            )

if __name__ == "__main__":
    main()