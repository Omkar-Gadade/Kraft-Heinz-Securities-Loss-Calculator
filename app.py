import streamlit as st
import pandas as pd

st.title("📊 Kraft-Heinz Securities Loss Calculator")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.write("### Raw Data Preview")
    st.dataframe(df.head())

    # ------------------------
    # YOUR EXISTING LOGIC HERE
    # ------------------------

    df["Trade Date"] = pd.to_datetime(df["Trade Date"], dayfirst=True)

    df["Purchases"] = df["Purchases"].fillna(0)
    df["Sales"] = df["Sales"].fillna(0)

    df["Qty"] = df["Purchases"] - df["Sales"]

    df = df[df["Transaction Type"].isin(["Purchase", "Sale"])]

    df = df.sort_values(["Entity", "Fund Name", "Trade Date"])

    # ---------- YOUR FUNCTIONS ----------
    from collections import deque

    def get_inflation(date):
        if date <= pd.Timestamp("2018-11-01"):
            return 12.59
        elif date <= pd.Timestamp("2019-02-21"):
            return 10.93
        elif date <= pd.Timestamp("2019-08-07"):
            return 4.04
        elif date == pd.Timestamp("2019-08-08"):
            return 1.33
        else:
            return 0.0

    def calculate_loss(buy, sell, qty):

        buy_price = buy["price"]
        sell_price = sell["Price per share"]

        buy_date = buy["date"]
        sell_date = sell["Trade Date"]

        inflation_buy = get_inflation(buy_date)
        inflation_sell = get_inflation(sell_date)

        if sell_date < pd.Timestamp("2018-11-02"):
            return 0

        elif sell_date <= pd.Timestamp("2019-08-07"):
            loss = min(
                inflation_buy - inflation_sell,
                buy_price - sell_price
            )

        elif sell_date <= pd.Timestamp("2019-11-05"):
            avg_price = 27.55
            loss = min(
                inflation_buy - inflation_sell,
                buy_price - avg_price,
                buy_price - sell_price
            )

        else:
            loss = min(
                inflation_buy,
                buy_price - 27.55
            )

        return max(loss, 0) * qty


    def compute_loss_for_fund(df_fund):

        inventory = deque()
        total_loss = 0

        for _, row in df_fund.iterrows():

            qty = row["Qty"]
            price = row["Price per share"]
            date = row["Trade Date"]

            if qty > 0:
                inventory.append({
                    "qty": qty,
                    "price": price,
                    "date": date
                })

            elif qty < 0:
                sell_qty = abs(qty)

                while sell_qty > 0 and inventory:

                    buy = inventory[0]
                    matched_qty = min(sell_qty, buy["qty"])

                    if date >= pd.Timestamp("2018-11-02"):
                        loss = calculate_loss(buy, row, matched_qty)
                        total_loss += loss

                    buy["qty"] -= matched_qty
                    sell_qty -= matched_qty

                    if buy["qty"] == 0:
                        inventory.popleft()

        return total_loss

    # ---------- RUN ----------
    results = []

    for (client, fund), group in df.groupby(["Entity", "Fund Name"]):

        loss = compute_loss_for_fund(group)

        results.append({
            "Client": client,
            "Fund": fund,
            "Loss": loss
        })

    result_df = pd.DataFrame(results)

    st.write("### Fund-wise Loss")
    st.dataframe(result_df)

     # Download button
    st.download_button(
        "⬇️ Download Results",
        result_df.to_csv(index=False),
        file_name="Fund_wise_Loss_results.csv"
    )

    client_loss = result_df.groupby("Client")["Loss"].sum().reset_index()

    st.write("### Client-wise Loss")
    st.dataframe(client_loss)

     # Download button
    st.download_button(
        "⬇️ Download Results",
        client_loss.to_csv(index=False),
        file_name="Client_wise_Loss_results.csv"
    )