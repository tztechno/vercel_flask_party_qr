from flask import Flask, render_template, request
import qrcode
import io
import base64
import csv

app = Flask(__name__)

# CSVファイルの読み込み
def load_data():
    data_list = []
    # CSVファイルのパス
    csv_file = 'guests.csv'
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_list.append(row)
    return data_list

# フォームのページ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data_list = load_data()  # CSVデータの読み込み
    user_id = request.form.get('id')
    name = request.form.get('name')

    user_data = None
    if user_id:
        for data in data_list:
            if data['id'] == user_id:
                user_data = data
                break

    elif name:
        for data in data_list:
            if data['name'] == name:
                user_data = data
                break

    else:
        return '氏名、ID、いずれかを入力してください。'

    if user_data:
        assigned_id = user_data['id']
        user_name = user_data['name']
        affiliation = user_data['comp']

        # QRコードを生成
        img = qrcode.make(assigned_id)
        buf = io.BytesIO()
        img.save(buf, 'PNG')
        buf.seek(0)

        # QRコードデータをbase64にエンコード
        qr_code_data = base64.b64encode(buf.getvalue()).decode('utf-8')

        # 検索結果を表示
        return render_template('success.html', name=user_name, affiliation=affiliation, assigned_id=assigned_id, qr_code_data=qr_code_data)
    else:
        return '該当するデータが見つかりませんでした。'

if __name__ == '__main__':
    app.run(debug=True)
