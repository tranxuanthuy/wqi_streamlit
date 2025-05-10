def predict_wqi(model, input_data):
    """
    Dự đoán giá trị WQI từ input gồm 4 biến đầu vào.

    Parameters:
        model: mô hình đã huấn luyện với các biến "BOD5", "COD", "TOC", "BHC", "Cd", "Cr6".
        input_data: dict chứa giá trị các biến cần thiết.

    Returns:
        Giá trị WQI dự đoán.
    """
    import pandas as pd

    feature_order = ["BOD5", "COD", "TOC", "BHC", "Cd", "Cr6"]
    input_df = pd.DataFrame([input_data])[feature_order]
    prediction = model.predict(input_df)[0]
    return prediction
