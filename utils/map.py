import folium
from folium.plugins import MarkerCluster, Fullscreen
from streamlit_folium import folium_static
def render_wqi_map(df):
    """Hiển thị bản đồ WQI từ DataFrame đã tính toán."""
    m = folium.Map(
        tiles="https://maps.becagis.vn/tiles/basemap/light/{z}/{x}/{y}.png",
        attr="BecaGIS",
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=8
    )

    Fullscreen(position="topright").add_to(m)
    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        color = row['WQI_Color']
        icon = folium.Icon(color=color, icon='ok-circle')

        popup_html = f"""
            <b>Trạm:</b> {row['station_id']}<br>
            <b>Ngày:</b> {row['date']}<br>
            <b>WQI:</b> {row['WQI']}<br>
            <b>Mức chất lượng:</b> {row['WQI_Level']}
        """
        
        iframe = folium.IFrame(popup_html, width=220, height=100) 
        popup = folium.Popup(iframe, max_width=400)

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,  # kích thước vòng tròn
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=popup
        ).add_to(cluster)

    # Thêm legend
    legend_html = '''
     <div style="position: absolute;
         bottom: 50px; left: 50px; width: 210px; height: 190px; 
         border:2px solid grey; z-index:9999; font-size:13px;
         background-color:white;
         padding: 10px;">
         <b>Chú giải WQI:</b><br>
         <i style="color:#7E0023;">■</i> Rất xấu (WQI < 25)<br>
         <i style="color:#FF0000;">■</i> Xấu (25–50)<br>
         <i style="color:#FF7E00;">■</i> Trung bình (50–70)<br>
         <i style="color:#FFFF00;">■</i> Khá (70–90)<br>
         <i style="color:#00E400;">■</i> Tốt (≥90)<br>
     </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Hiển thị trong Streamlit
    folium_static(m, width=900, height=600)