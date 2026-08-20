import gradio as gr
import joblib
import pandas as pd
import numpy as np

# =========================
# Load Model
# =========================
models = joblib.load("model.pkl")


# =========================
# Dropdown Options
# =========================

inquiry_topics = [
    "Return & Refund",
    "Product Feedback",
    "Warranty Claim",
    "Data Security",
    "Promotions & Offers",
    "Shipping Status",
    "Account Management",
    "Billing Inquiry",
    "Technical Support"
]

products = [
    "Smartphone",
    "Speaker",
    "Tablet",
    "Printer",
    "Charger",
    "Smartwatch",
    "Camera",
    "Laptop",
    "Router",
    "Headphones"
]


# =========================
# Prediction Function
# =========================

def predict(
    satisfaction,
    wait_time,
    support_quality,
    handle_time,
    inquiry_topic,
    product
):
    try:

        # Get feature names from training data
        feature_names = X.columns.tolist() if 'X' in globals() else []

        if len(feature_names) == 0:
            return (
                "❌ Error",
                "N/A",
                "Training feature names (X) are not available."
            )

        # Create empty row
        data = pd.DataFrame(
            0.0,
            index=[0],
            columns=feature_names
        )

        # =========================
        # Numerical Features
        # =========================

        if "Customer Satisfaction & Recommendations (Rating)" in data.columns:
            data["Customer Satisfaction & Recommendations (Rating)"] = float(
                satisfaction
            )

        if "Average Wait Time (seconds)" in data.columns:
            data["Average Wait Time (seconds)"] = float(
                wait_time
            )

        if "Quality of Recent Support (Rating)" in data.columns:
            data["Quality of Recent Support (Rating)"] = float(
                support_quality
            )

        if "Call Handle Time (minutes)" in data.columns:
            data["Call Handle Time (minutes)"] = float(
                handle_time
            )


        # =========================
        # Categorical Features
        # =========================

        # One-Hot Encoding style
        inquiry_column = f"Customer Inquiry Topic_{inquiry_topic}"

        if inquiry_column in data.columns:
            data[inquiry_column] = 1.0

        product_column = f"Product Discussed_{product}"

        if product_column in data.columns:
            data[product_column] = 1.0


        # =========================
        # Scaling
        # =========================

        if 'scaler' in globals():
            data_input = scaler.transform(data)
        else:
            data_input = data.values.astype(np.float32)


        # =========================
        # Prediction
        # =========================

        prediction_raw = models.predict(data_input)

        probability = float(
            np.asarray(prediction_raw).flatten()[0]
        )

        probability_percent = probability * 100


        # =========================
        # Result
        # =========================

        if probability >= 0.5:

            result = "⚠️ HIGH RISK"

            recommendation = (
                "🔴 Immediate Action Recommended\n\n"
                "• Review the customer's issue carefully.\n"
                "• Try to completely resolve the issue during this call.\n"
                "• Reduce waiting time if possible.\n"
                "• Consider a follow-up with the customer.\n"
                "• Pay special attention to the customer's satisfaction."
            )

        else:

            result = "✅ LOW RISK"

            recommendation = (
                "🟢 No Immediate Action Required\n\n"
                "• Current support appears effective.\n"
                "• Maintain the current service quality.\n"
                "• Continue monitoring customer satisfaction.\n"
                "• No immediate follow-up is required."
            )


        return (
            result,
            f"{probability_percent:.2f}%",
            recommendation
        )


    except Exception as e:

        return (
            "❌ ERROR",
            "N/A",
            str(e)
        )


# =========================
# Custom CSS
# =========================

css = """
body {
    background: #f5f7fb;
}

.gradio-container {
    max-width: 1100px !important;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 36px !important;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 25px;
}

.input-box {
    border-radius: 14px !important;
    border: 1px solid #e5e7eb !important;
}

.result-box {
    border-radius: 14px !important;
    min-height: 100px;
}

.predict-btn {
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

.footer {
    text-align: center;
    color: #9ca3af;
    margin-top: 20px;
}
"""


# =========================
# UI
# =========================

with gr.Blocks(
    theme=gr.themes.Soft(),
    css=css
) as demo:

    gr.Markdown(
        """
        <div class="title">
        📞 Repeat Calls Prediction
        </div>

        <div class="subtitle">
         prediction of customer repeat calls
        </div>
        """
    )


    with gr.Row():

        # =====================
        # Customer Information
        # =====================

        with gr.Column():

            gr.Markdown("### 👤 Customer Information")

            satisfaction = gr.Number(
                label="Customer Satisfaction",
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                elem_classes="input-box"
            )

            inquiry_topic = gr.Dropdown(
                choices=inquiry_topics,
                label="Customer Inquiry Topic",
                value="Technical Support",
                elem_classes="input-box"
            )

            product = gr.Dropdown(
                choices=products,
                label="Product Discussed",
                value="Laptop",
                elem_classes="input-box"
            )


        # =====================
        # Call Information
        # =====================

        with gr.Column():

            gr.Markdown("### 📞 Call Information")

            wait_time = gr.Number(
                label="Average Wait Time (seconds)",
                minimum=0,
                value=60,
                elem_classes="input-box"
            )

            support_quality = gr.Number(
                label="Quality of Support",
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                elem_classes="input-box"
            )

            handle_time = gr.Number(
                label="Call Handle Time (minutes)",
                minimum=0,
                value=5,
                elem_classes="input-box"
            )


    gr.Markdown("### 🔮 Prediction")


    predict_btn = gr.Button(
        "🚀 Predict Repeat Call",
        variant="primary",
        size="lg",
        elem_classes="predict-btn"
    )


    with gr.Row():

        prediction_output = gr.Textbox(
            label="Prediction",
            interactive=False,
            elem_classes="result-box"
        )

        probability_output = gr.Textbox(
            label="Repeat Call Probability",
            interactive=False,
            elem_classes="result-box"
        )


    recommendation_output = gr.Textbox(
        label="💡 Recommendation",
        lines=7,
        interactive=False,
        elem_classes="result-box"
    )


    # =========================
    # Button Action
    # =========================

    predict_btn.click(
        fn=predict,
        inputs=[
            satisfaction,
            wait_time,
            support_quality,
            handle_time,
            inquiry_topic,
            product
        ],
        outputs=[
            prediction_output,
            probability_output,
            recommendation_output
        ]
    )


    gr.Markdown(
        """
        <div class="footer">
        Repeat Calls Prediction • Machine Learning Project
        </div>
        """
    )


# =========================
# Launch
# =========================

demo.launch(share=True)