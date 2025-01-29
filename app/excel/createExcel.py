
import os
import pandas as pd

def createExcelOrder(orderlist,filename:str):

    if not os.path.exists("excel_files"):
        os.makedirs("excel_files")

    order_list= []

    for order in orderlist.orders:
        order_list.append({
            "ID": order.id,
            "Title": order.title,
            "Price": order.price,
            "Weight": order.weight,
        })
    
    df= pd.DataFrame(order_list)

    filepath = os.path.join("excel_files", filename)
    with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Orders")
    
    return filepath