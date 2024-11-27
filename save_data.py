from sqlalchemy import create_engine, text
import pandas as pd

def SQL_save(path):
    # 配置数据库连接字符串
    conn_str = 'mssql+pyodbc://ysx:123456@127.0.0.1:1433/nga?driver=ODBC+Driver+13+for+SQL+Server'

    # 创建引擎
    engine = create_engine(conn_str)

    # 读取 CSV 文件
    data_df = pd.read_csv(path)

    # 插入数据到数据库
    try:
        with engine.connect() as connection:
            data_df.to_sql('test', engine, if_exists='append', index=False, schema='dbo')
        print("数据插入成功！")
    except Exception as e:
        print(f"插入失败: {e}")

if __name__ == '__main__':
    path='data.csv'
    SQL_save(path)
