import  pandas as pd    

def item_consumer(mat,item,person):
    if(mat[item][person] == 0):
        mat[item][person] = 1
    return mat

def get_individual_prices(mat,df_items,df_price):
    rows = len(mat)
    cols = len(mat[0])
    price = []
    total_gst = df_price['CGST'][0] + df_price['SGST'][0]
    for i in range(rows):
        counter = 0
        for j in range(cols):
            if (mat[i][j] == 1):
                counter += 1
        gst_amt = df_items['Prices'][i]*total_gst/100
        price.append((df_items['Prices'][i] + gst_amt)/counter)
    for i in range(rows):
        for j in range(cols):
            if (mat[i][j] == 1):
                mat[i][j] = price[i]
    amt = pd.DataFrame(mat).round(2)
    return amt