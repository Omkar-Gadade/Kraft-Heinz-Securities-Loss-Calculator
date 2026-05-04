# 📊 Securities Litigation Loss Calculator (Kraft Heinz Settlement)

## 🚀 Overview

This project implements a **loss calculation engine** for the Kraft Heinz Securities Litigation Settlement.
It computes **recognized losses** for investors based on:

* FIFO (First-In-First-Out) transaction matching
* Date-based artificial inflation (Table A)
* Settlement-specific loss formulas
* Fund-level and client-level aggregation

The solution is built using **Python and Streamlit**, enabling users to upload transaction data and compute losses through a simple web interface.

---

## 🧠 Key Concepts Implemented

### 1. FIFO Matching

Transactions are matched using First-In-First-Out logic:

* Oldest purchases are matched with earliest sales
* Ensures accurate buy-sell pairing for loss calculation

---

### 2. Artificial Inflation (Table A)

The settlement defines inflation values based on time periods:

| Date Range                 | Inflation |
| -------------------------- | --------- |
| Nov 6, 2015 – Nov 1, 2018  | 12.59     |
| Nov 2, 2018 – Feb 21, 2019 | 10.93     |
| Feb 22, 2019 – Aug 7, 2019 | 4.04      |
| Aug 8, 2019                | 1.33      |
| After Aug 8, 2019          | 0.00      |

Inflation is mapped as:

```
Trade Date → Inflation Value
```

---

### 3. Loss Calculation Rules

Loss per share is calculated as:

```
min(
    Inflation_buy - Inflation_sell,
    Buy Price - Sell Price
)
```

Additional conditions:

| Case | Condition                        | Rule                        |
| ---- | -------------------------------- | --------------------------- |
| A    | Sale before Nov 2, 2018          | Loss = 0                    |
| B    | Sale before Aug 8, 2019          | Basic min rule              |
| C    | Sale between Aug 8 – Nov 5, 2019 | Includes avg price cap      |
| D    | Holding after Nov 5, 2019        | Uses inflation vs avg price |

---

### 4. Average Price Adjustment

For certain cases, loss is capped using an average price:

```
Average Price = 27.55
```

Used in post-disclosure scenarios to prevent overstated losses.

---

### 5. Aggregation Logic

* Loss is computed at **fund level**
* Aggregated to **client level**

```
Client Loss = Sum of all fund losses
```

---

## 📂 Input Format

The input Excel file must contain:

* `Entity`
* `Fund Name`
* `Transaction Type` (Purchase / Sale)
* `Purchases`
* `Sales`
* `Price per share`
* `Trade Date`

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🌐 Features

* Upload Excel file
* Automatic FIFO matching
* Inflation-based loss calculation
* Fund-wise and client-wise outputs
* Download results as CSV

---

## 📊 Output

* **Fund-wise Loss**
* **Client-wise Total Loss**

---

## 🧪 Example Workflow

Upload transaction data →
System applies FIFO →
Maps inflation →
Calculates loss →
Outputs final results

---

## ⚠️ Notes

* Only common stock transactions are considered
* Options (calls/puts) are excluded as they are not present in the dataset
* Inflation values are fixed as per settlement notice

---

## 💡 Tech Stack

* Python
* Pandas
* Streamlit

---

## 🎯 Conclusion

This project demonstrates how a **legal settlement framework** can be translated into a **data-driven financial model**, combining:

* Financial reasoning
* Algorithmic implementation
* Interactive web deployment

---

## 📎 Author

Omkar Gadade
