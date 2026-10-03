import streamlit as st

# Cấu hình giao diện trang Streamlit
st.set_page_config(
    page_title="Ứng dụng Tính Lãi Tiết Kiệm", page_icon="💰", layout="centered"
)

st.title("💰 Ứng dụng Tính Lãi Tiết Kiệm Ngân Hàng")
st.write(
    "Nhập thông tin khoản tiết kiệm của bạn ở thanh bên (sidebar) để xem kết"
    " quả chi tiết."
)

# Sidebar chứa các ô nhập liệu cho người dùng
st.sidebar.header("⚙️ Thông tin khoản gửi")

principal = st.sidebar.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=1_000_000.0,
    value=50_000_000.0,
    step=1_000_000.0,
    format="%,.0f",
)

term_months = st.sidebar.number_input(
    "Kỳ hạn gửi (tháng)", min_value=1, max_value=360, value=12, step=1
)

annual_rate = st.sidebar.number_input(
    "Lãi suất (%/năm)", min_value=0.1, max_value=50.0, value=6.0, step=0.1
)

interest_type = st.sidebar.radio("Chọn hình thức tính lãi", ("Lãi đơn", "Lãi kép"))

payout_method = st.sidebar.selectbox(
    "Hình thức nhận lãi", ("Cuối kỳ", "Hàng tháng", "Hàng quý")
)

# Kiểm tra logic kỳ hạn và hình thức nhận lãi
valid_calculation = True
if payout_method == "Hàng quý" and term_months < 3:
  st.sidebar.error(
      "⚠️ Kỳ hạn gửi phải từ 3 tháng trở lên nếu chọn nhận lãi hàng quý!"
  )
  valid_calculation = False
elif payout_method == "Hàng tháng" and term_months < 1:
  st.sidebar.error("⚠️ Kỳ hạn gửi phải từ 1 tháng trở lên!")
  valid_calculation = False

# Xử lý tính toán khi dữ liệu hợp lệ
if valid_calculation:
  r_annual = annual_rate / 100.0
  t_years = term_months / 12.0

  total_interest = 0.0
  total_amount = 0.0
  periodic_interest = 0.0

  if interest_type == "Lãi đơn":
    # Công thức lãi đơn tổng cộng: I = P * r * (tháng / 12)
    total_interest = principal * r_annual * t_years
    total_amount = principal + total_interest

    # Tính tiền lãi định kỳ theo lựa chọn
    if payout_method == "Hàng tháng":
      periodic_interest = total_interest / term_months
    elif payout_method == "Hàng quý":
      num_quarters = term_months / 3.0
      periodic_interest = total_interest / num_quarters
    else:  # Cuối kỳ
      periodic_interest = total_interest

  else:  # Lãi kép
    # Lãi kép tính dựa trên kỳ ghép lãi (hàng tháng hoặc hàng quý)
    if payout_method == "Hàng tháng":
      r_period = r_annual / 12.0
      n_periods = term_months
      total_amount = principal * ((1 + r_period) ** n_periods)
      total_interest = total_amount - principal
      periodic_interest = (
          total_interest / n_periods if n_periods > 0 else 0
      )  # Hoặc lãi tháng thực tế

    elif payout_method == "Hàng quý":
      r_period = r_annual / 4.0
      n_periods = term_months / 3.0
      total_amount = principal * ((1 + r_period) ** n_periods)
      total_interest = total_amount - principal
      periodic_interest = total_interest / n_periods if n_periods > 0 else 0

    else:  # Cuối kỳ (mặc định ghép lãi hàng tháng nếu không rút định kỳ)
      r_period = r_annual / 12.0
      n_periods = term_months
      total_amount = principal * ((1 + r_period) ** n_periods)
      total_interest = total_amount - principal
      periodic_interest = total_interest

  # Hiển thị kết quả
  st.markdown("---")
  st.subheader("📊 Kết quả tính toán chi tiết")

  col1, col2, col3 = st.columns(3)

  with col1:
    if payout_method != "Cuối kỳ":
      st.metric(
          label=f"Tiền lãi định kỳ ({payout_method.lower()})",
          value=f"{periodic_interest:,.0f} VNĐ",
      )
    else:
      st.metric(
          label="Tiền lãi định kỳ", value="Nhận cuối kỳ (Không chia nhỏ)"
      )

  with col2:
    st.metric(label="Tổng tiền lãi nhận được", value=f"{total_interest:,.0f} VNĐ")

  with col3:
    st.metric(
        label="Tổng số tiền (Gốc + Lãi)", value=f"{total_amount:,.0f} VNĐ"
    )

  # Bảng tóm tắt thông tin đầu vào
  st.markdown("---")
  st.markdown("### 📋 Tóm tắt thông tin khoản gửi")
  st.info(f"""
    - **Số tiền gửi ban đầu:** {principal:,.0f} VNĐ
    - **Kỳ hạn gửi:** {term_months} tháng
    - **Lãi suất áp dụng:** {annual_rate}% / năm
    - **Hình thức tính lãi:** {interest_type}
    - **Hình thức nhận lãi:** {payout_method}
    """)
