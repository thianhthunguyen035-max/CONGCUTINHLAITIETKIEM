import streamlit as st
st.image("logo.jpg")

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("CÔNG CỤ TÍNH TIỀN GỬI TIẾT KIỆM_NGUYỄN THỊ ANH THƯ")
st.caption("Tính toán tiền lãi theo kỳ hạn, lãi suất và hình thức nhận lãi.")


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        value=12,
        step=1
    )

col3, col4 = st.columns(2)

with col3:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

with col4:
    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

loai_lai = st.radio(
    "Phương thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_nam = lai_suat / 100

    # Tổng số tháng
    so_thang = int(ky_han)

    # Tổng số kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Cuối kỳ":
        so_ky = 1
        thang_moi_ky = so_thang
    elif hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = so_thang
        thang_moi_ky = 1
    else:  # Hàng quý
        so_ky = (so_thang + 2) // 3
        thang_moi_ky = 3

    # ==========================================
    # LÃI ĐƠN
    # ==========================================
    if loai_lai == "Lãi đơn":

        # Lãi đơn:
        # Tiền lãi = Gốc × lãi suất năm × số tháng / 12
        tong_lai = tien_gui * lai_nam * so_thang / 12

        # Lãi thực tế chia đều theo kỳ nhận
        lai_moi_ky = tong_lai / so_ky

        tong_tien = tien_gui + tong_lai

        # Tạo bảng chi tiết
        rows = []

        for i in range(1, so_ky + 1):
            thang_ket_thuc = min(i * thang_moi_ky, so_thang)

            lai_ky = (
                tien_gui
                * lai_nam
                * (thang_ket_thuc - (i - 1) * thang_moi_ky)
                / 12
            )

            rows.append({
                "Kỳ": i,
                "Thời điểm": f"Tháng {thang_ket_thuc}",
                "Tiền lãi": lai_ky,
                "Gốc": tien_gui,
                "Tổng nhận": tien_gui + lai_ky
            })

    # ==========================================
    # LÃI KÉP
    # ==========================================
    else:

        # Lãi suất theo tháng
        lai_thang = lai_nam / 12

        rows = []
        tong_lai = 0

        if hinh_thuc_nhan_lai == "Cuối kỳ":

            # Toàn bộ tiền lãi nhập gốc cuối kỳ
            tong_tien = tien_gui * ((1 + lai_thang) ** so_thang)
            tong_lai = tong_tien - tien_gui

            rows.append({
                "Kỳ": 1,
                "Thời điểm": f"Tháng {so_thang}",
                "Tiền lãi": tong_lai,
                "Gốc": tien_gui,
                "Tổng nhận": tong_tien
            })

            lai_moi_ky = tong_lai

        elif hinh_thuc_nhan_lai == "Hàng tháng":

            so_du = tien_gui

            for i in range(1, so_thang + 1):
                lai_ky = so_du * lai_thang
                so_du += lai_ky
                tong_lai += lai_ky

                rows.append({
                    "Kỳ": i,
                    "Thời điểm": f"Tháng {i}",
                    "Tiền lãi": lai_ky,
                    "Gốc": tien_gui,
                    "Tổng nhận": so_du
                })

            tong_tien = so_du
            lai_moi_ky = tong_lai / so_thang

        else:  # Hàng quý

            so_du = tien_gui
            so_quy = so_thang // 3
            thang_le = so_thang % 3

            for i in range(1, so_quy + 1):

                # Lãi kép theo 3 tháng
                lai_ky = so_du * ((1 + lai_thang) ** 3 - 1)

                so_du += lai_ky
                tong_lai += lai_ky

                rows.append({
                    "Kỳ": i,
                    "Thời điểm": f"Tháng {i * 3}",
                    "Tiền lãi": lai_ky,
                    "Gốc": tien_gui,
                    "Tổng nhận": so_du
                })

            # Xử lý số tháng lẻ nếu kỳ hạn không chia hết cho 3
            if thang_le > 0:
                lai_ky = so_du * (
                    (1 + lai_thang) ** thang_le - 1
                )

                so_du += lai_ky
                tong_lai += lai_ky

                rows.append({
                    "Kỳ": so_quy + 1,
                    "Thời điểm": f"Tháng {so_thang}",
                    "Tiền lãi": lai_ky,
                    "Gốc": tien_gui,
                    "Tổng nhận": so_du
                })

            tong_tien = so_du
            lai_moi_ky = tong_lai / len(rows)


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_money(lai_moi_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(tong_lai)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Tiền gốc",
            format_money(tien_gui)
        )

    with col4:
        st.metric(
            "Tổng tiền gốc + lãi",
            format_money(tong_tien)
        )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.subheader("📝 Thông tin khoản gửi")

    summary = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức nhận lãi",
            "Phương thức tính",
            "Tổng tiền lãi",
            "Tổng tiền nhận"
        ],
        "Giá trị": [
            format_money(tien_gui),
            f"{so_thang} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc_nhan_lai,
            loai_lai,
            format_money(tong_lai),
            format_money(tong_tien)
        ]
    })

    st.table(summary)

    # =========================
    # CHI TIẾT THEO TỪNG KỲ
    # =========================
    st.subheader("📅 Chi tiết tiền lãi theo kỳ")

    df = pd.DataFrame(rows)

    df["Tiền lãi"] = df["Tiền lãi"].apply(format_money)
    df["Gốc"] = df["Gốc"].apply(format_money)
    df["Tổng nhận"] = df["Tổng nhận"].apply(format_money)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # GHI CHÚ
    # =========================
    st.info(
        "Lưu ý: Đây là công cụ mô phỏng theo lãi suất người dùng nhập. "
        "Lãi suất thực tế của ngân hàng, cách làm tròn tiền lãi và quy định "
        "nhập lãi vào gốc có thể khác."
    )
